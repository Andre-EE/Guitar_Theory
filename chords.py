from collections import deque

from helper import Helper
from helper import CollectionHelper

class Chord(Helper):
    def __init__(self, root: str, quality: str, notes: str):

        super().__init__(root)

        self._quality       = quality

        self._notes         = notes
        self._alt_notes     = []

        self._flat_notes    = []
        self._sharp_notes   = []

    @property
    def root(self):
        return self.tonic

    @property
    def alt_root(self):
        return self.alt_tonic

    @property
    def quality(self):
        return self._quality

    @property
    def name(self):
        return (self.root, self.quality)

    @property
    def notes(self):
        return self._notes
    @notes.setter
    def notes(self, value: list):
        self._alt_notes = []
        self._notes     = value
    
    @property
    def alt_notes(self):
        if len(self._alt_notes) == 0:
            if self.is_flat(): 
                self._alt_notes = self.sharp_notes
            else:
                self._alt_notes = self.flat_notes
        return self._alt_notes    
    
    @property
    def flat_notes(self):
        if len(self._flat_notes) == 0:
            for note in self.notes:
                if self.is_sharp(note) or self.is_flat(note):
                    chromatic_scale_index = self.get_chromatic_scale_index(note)
                    self._flat_notes.append(self.chromatic_scale[chromatic_scale_index + 1] + 'b')
                else:
                    self._flat_notes.append(note)
        return self._flat_notes

    @property
    def sharp_notes(self):
        if len(self._sharp_notes) == 0:
            for note in self.notes:
                if self.is_sharp(note) or self.is_flat(note):
                    chromatic_scale_index = self.get_chromatic_scale_index(note)
                    self._sharp_notes.append(self.chromatic_scale[chromatic_scale_index])
                else:
                    self._sharp_notes.append(note)
        return self._sharp_notes

    def last_access_key(self, value: tuple):
        if ('b' in value[0] and self.is_sharp()) or \
            ('#' in value[0] and self.is_flat()):
            self.notes  = self.alt_notes
            self.tonic  = self.alt_tonic

    def __str__(self):
        notes_str       = ', '.join([f"{note:<2}" for note in self.notes])
        alt_notes_str   = ', '.join([f"{note:<2}" for note in self.alt_notes])
        if self.alt_root is not None:
           alt_root_str  = f"({self.alt_root:<2})"
        else:
           alt_root_str  = '    '
           
        return f"{self.root: <2} {alt_root_str} {self.quality:<16}: [{notes_str:<14}]   [({alt_notes_str:<14})]"


class Chords(CollectionHelper):
    def __init__(self):

        super().__init__()
        
        self.qualities = []
        self.generate_chords()

    def generate_chords_for_root(self, root: str):
        
        root_index = self.chromatic_scale.index(root)
        chromatic_scale_in_key = deque(self.chromatic_scale)
        chromatic_scale_in_key.rotate(-root_index)

        perfect_unison = chromatic_scale_in_key[0]
        minor_2nd      = chromatic_scale_in_key[1]
        major_2nd      = chromatic_scale_in_key[2]
        minor_3rd      = chromatic_scale_in_key[3]
        major_3rd      = chromatic_scale_in_key[4]
        perfect_4th    = chromatic_scale_in_key[5]
        augmented_4th  = chromatic_scale_in_key[6]
        diminished_5th = chromatic_scale_in_key[6]
        perfect_5th    = chromatic_scale_in_key[7]
        minor_6th      = chromatic_scale_in_key[8]
        major_6th      = chromatic_scale_in_key[9]
        minor_7th      = chromatic_scale_in_key[10]
        major_7th      = chromatic_scale_in_key[11]

        chord_dictionary_for_root = {}

        chord_dictionary_for_root['major']           = [perfect_unison,  major_3rd,     perfect_5th               ]
        chord_dictionary_for_root['minor']           = [perfect_unison,  minor_3rd,     perfect_5th               ]
        chord_dictionary_for_root['major_7th']       = [perfect_unison,  major_3rd,     perfect_5th,     major_7th]
        chord_dictionary_for_root['minor_7th']       = [perfect_unison,  minor_3rd,     perfect_5th,     minor_7th]
        chord_dictionary_for_root['dominant_7th']    = [perfect_unison,  major_3rd,     perfect_5th,     minor_7th]
        chord_dictionary_for_root['sus2']            = [perfect_unison,  major_2nd,     perfect_5th               ]
        chord_dictionary_for_root['sus4']            = [perfect_unison,  perfect_4th,   perfect_5th               ]
        chord_dictionary_for_root['diminished']      = [perfect_unison,  minor_3rd,     diminished_5th            ]
        chord_dictionary_for_root['half_diminished'] = [perfect_unison,  minor_3rd,     diminished_5th,  minor_7th]

        return chord_dictionary_for_root

    def generate_chords(self):
        for root in self.chromatic_scale:    
            chord_dictionary_for_root = self.generate_chords_for_root(root)
            for chord_quality, chord_notes in chord_dictionary_for_root.items():
                current_chord = Chord(root, chord_quality, chord_notes)
                chord_dict_key = (root, chord_quality)
                self._instances[chord_dict_key] = current_chord
                if current_chord.alt_root is not None:
                    chord_alt_dict_key = (current_chord.alt_root, chord_quality)
                    self._instances[chord_alt_dict_key] = current_chord 

        self.qualities = list(chord_dictionary_for_root.keys())

    def get_qualities(self):
        return self.qualities

    def get_chord(self, chord_dict_key: tuple):
        return self[chord_dict_key]
    
    def __getitem__(self, dict_key: tuple):
        item = self._instances.get(dict_key, None)
        item.last_access_key(dict_key)
        return item