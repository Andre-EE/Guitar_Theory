from collections import deque

from chords     import Chord, Chords
from fretboard  import Fretboard
from helper     import CollectionHelper

class Voicing:
    def __init__(self, chord: Chord, fretboard: Fretboard, base_shape: dict = None):

        self.chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        self._name              = None
        self.chord              = chord
        self.fretboard          = fretboard
        self.base_shape         = base_shape
        self.low_fret           = None
        self.high_fret          = None

        self.sub_board          = [[None]*self.fretboard.number_of_frets for i in range(6)]
        
        self.indices_by_note    = {}
        self.indices_by_string  = {}
        self.note_list          = []
        
        self.voice_chord()

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value: tuple):
        if self._name == None:
            self._name = value

    @property
    def shape(self):
        return self.indices_by_string

    def get_chromatic_scale_in_key(self, key):
        key_index = self.chromatic_scale.index(key)
        chromatic_scale_in_key = deque(self.chromatic_scale)
        chromatic_scale_in_key.rotate(-key_index)
        return chromatic_scale_in_key

    def voice_chord(self):
        if self.base_shape is None:
            self.voice_open_chord()
        else:
            self.voice_chord_by_shape()

        if len(self.indices_by_string) > 0:
            # note_index[0][1] pulls out the 2nd item in the tuple, which is the fret
            frets = [note_index[0][1] for note_index in self.indices_by_string.values()]
            self.low_fret   = min(frets)
            self.high_fret  = max(frets)

    def voice_open_chord(self):
                
        # step 1: gather the (string, fret) indices of all notes that appear in the chord
        for note in self.chord.notes:
            note_indices = self.fretboard.note_directory[note].copy()
            # iterate over copy of the list so that it can be changed without disrupting the loop
            for string, fret in note_indices.copy():
                if fret not in range(0,4):
                    note_indices.remove((string, fret))
            self.indices_by_note[note] = note_indices

        # step 2: find the index of the chord's bass (root) note
        root_note_string, root_note_fret = max(self.indices_by_note[self.chord.root], key = lambda x : x[0])

        # step 3: remove any notes that are lower than the bass (root) note
        for note, note_indices in self.indices_by_note.items():
            for string, fret in note_indices.copy():
                if string > root_note_string:
                    note_indices.remove((string, fret))
                elif string == root_note_string and fret < root_note_fret:
                    note_indices.remove((string, fret))
            
        # step 4: organize notes by string now
        for note, note_indices in self.indices_by_note.items():
            for string, fret in note_indices:
                self.indices_by_string.setdefault(string, []).append((string, fret))
        self.indices_by_string = dict(sorted(self.indices_by_string.items()))

        # step 5: find strings that have multiple notes
        overloaded_string_notes = [note_list for note_list in self.indices_by_string.values() if len(note_list) > 1]
        # step 6: find notes where the base note appears on multiple strings
        duplicated_notes = [keys for keys in self.indices_by_note.values() if len(keys) > 1]
        # step 7: find notes that appear on both overloaded strings and who's base note appears on another string
        redundant_notes = self.intersection(overloaded_string_notes, duplicated_notes)

        # at this point redundant_notes is a list of lists, where the sublists contain notes that can be removed. they can 
        # be removed for 2 reasons: they appear on overloaded strings, and the base note appears elsewhere in the chord

        # step 8: remove redundant notes on each string. when there are multiple options, remove the note on the higher fret
        for redundant_notes_by_string in redundant_notes:
            note_index_to_remove = max(redundant_notes_by_string, key = lambda x : x[1])
            for key, value in self.indices_by_note.items():
                if note_index_to_remove in value:
                    value.remove(note_index_to_remove)
            for key, value in self.indices_by_string.items():
                if note_index_to_remove in value:
                    value.remove(note_index_to_remove)

        for key, note_index in self.indices_by_string.items():
            for string, fret in note_index:
                note = self.fretboard.fretboard[string][fret]
                self.note_list.append(note)
                self.sub_board[string][fret] = note

    def voice_chord_by_shape(self):

        root_note_string = max(self.base_shape, key=lambda string: self.base_shape.get(string))
        root_note_string, root_note_fret = self.base_shape[root_note_string][0]
        base_shape_root_note = self.fretboard.fretboard[root_note_string][root_note_fret]

        chromatic_scale_in_key = self.get_chromatic_scale_in_key(base_shape_root_note.base)
        base_shape_to_new_root_delta = chromatic_scale_in_key.index(self.chord.root)

        for key, note_index in self.base_shape.items():
            note_string, note_fret = note_index[0]
            new_note_index = (note_string, note_fret + base_shape_to_new_root_delta)
            self.indices_by_string[key] = [new_note_index]
        
        for key, note_index in self.indices_by_string.items():
            for note_string, note_fret in note_index:
                note = self.fretboard.fretboard[note_string][note_fret]
                self.note_list.append(note)
                self.sub_board[note_string][note_fret] = note

    def intersection(self, list_of_lists1, list_of_lists2):
        intersection_list = []
        for sublist1 in list_of_lists1:
            common_elements = []
            for element in sublist1:
                for sublist2 in list_of_lists2:
                    if element in sublist2:
                        common_elements.append(element)
            intersection_list.append(common_elements)
        return intersection_list

    def __str__(self):
        print_string = [f'{self.chord.root}_{self.chord.quality}: \n\n']

        for string in self.sub_board:
            open_fret = True
            for note in string:
                name_string = '--' if note is None else note.name
                if open_fret:
                    open_fret = False
                    print_string.append(f"{name_string: <6}{'|': <4}")
                else:
                    print_string.append(f"{name_string: <10}")
            print_string.append('\n')

        for fret in range(len(string)):
            if fret == 0:
                print_string.append(f"{'': <6}{' ': <4}")
            elif fret in [3, 5, 7, 9, 12]:
                print_string.append(f"{fret: <10}")
            else:
                print_string.append(f"{'': <10}")
        print_string.append('\n')

        return ''.join(print_string)

class Voicings(CollectionHelper):
    def __init__(self, chords: Chords, fretboard: Fretboard):

        super().__init__()

        self.chords             = chords
        self.fretboard          = fretboard
        self.caged_notes        = ['C', 'A', 'G', 'E', 'D']
        self.basic_qualities    = self.chords.get_qualities()

        self.generate_open_voicings()
        self.generate_voicings_based_on_shape()

    def generate_open_voicings(self):
        for root in self.caged_notes + ['B']:
            for quality in self.basic_qualities:
                voicing = Voicing(self.chords[(root, quality)], self.fretboard)
                chord_voice_dict_key = (root, quality, 'open')
                voicing.name = chord_voice_dict_key
                self._instances[chord_voice_dict_key] = voicing

    def generate_voicings_based_on_shape(self):
        for root in self.chromatic_scale:
            for base_shape_root in self.caged_notes:
                for quality in self.basic_qualities:
                    # avoid G and C_minor shapes
                    if base_shape_root not in [root, 'G'] and (base_shape_root, quality) != ('C', 'minor'):
                        chord_to_voice = self.chords[(root, quality)]
                        base_shape = self._instances[(base_shape_root, quality, 'open')].shape
                        voicing = Voicing(chord_to_voice, self.fretboard, base_shape)
                        chord_voice_dict_key = (root, quality, base_shape_root)
                        voicing.name = chord_voice_dict_key
                        self._instances[chord_voice_dict_key] = voicing

    def get_voicing_instances_for_chord(self, chord):
        result = {}
        for chord_voice_key, chord_voicing in self._instances.items():
            if chord_voicing.chord.name == chord:
                result[chord_voice_key] = chord_voicing
        return result
    
    def get_list_of_voicing_names_for_chord(self, chord):
        voicing_name_list = []
        voicing_name_list = list(self.get_voicing_instances_for_chord(chord).keys())
        voicing_name_list.sort(key = lambda voicing_name: self[voicing_name].low_fret)
        return voicing_name_list
    
    def get_chord_voice(self, chord_root, chord_quality, shape: str = 'E'):
        return self[(chord_root, chord_quality, shape)]
    
    def __getitem__(self, dict_key: tuple):
        item = self._instances.get(dict_key, None)
        return item