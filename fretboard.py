from notes import Notes

class Fretboard():
    def __init__(self, notes: Notes, number_of_frets: int = 15):

        self.notes = notes
        self.fretboard = [[] for i in range(6)]
        self.note_directory = {}
        self.open_position_notes = []

        self.chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        self.number_of_frets = number_of_frets

        self.generate_strings()
        self.generate_open_notes()
        self.generate_note_directory()

    def generate_strings(self, number_of_frets: int = 15, tuning: str = 'standard'):
        
        # fills in self.fretboard (list of lists): 
        # the outer list contains 6 lists, one for each string,
        # and each of these lists contain notes corresponding to the number of frets
        # only standard tuning is supported

        if tuning == 'standard':
            open_notes = ['E2','A2','D3','G3','B3','E4']
            open_notes.reverse()

        for string in range(6):
            open_note = open_notes[string]
            note_index = self.notes[open_note].index
            for fret in range(number_of_frets):
                note = self.notes.get_note_by_index(note_index + fret)
                note.fret_list = (string, fret)
                self.fretboard[string].append(note)

    def generate_open_notes(self):
        for string in range(6):
            self.open_position_notes.append(self.fretboard[string][0:4])

    def generate_note_directory(self):
        
        all_notes = ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B']

        # create a key:value pair of a music note and empty list
        for note in all_notes:
            self.note_directory[note] = []

        # iterate through each note on the fretboard and add entries of the fret list
        # to the directory. 'extend' adds list entries vs adding the list. 
        for string in self.fretboard:
            for note in string:
                self.note_directory[note.base].extend(note.fret_list)
                if note.alt_name is not None:
                    self.note_directory[note.alt_base].extend(note.fret_list)
        
        # remove duplicate note directory entries. final result is dict of sets
        for note in all_notes:
            self.note_directory[note] = sorted(set(self.note_directory[note]))

    def print_open_notes(self):
        for string in self.fretboard:
            for note in string[0:4]:
                print(f"{note.name: <10}", end = "")
            print('')
        print('')

    def print_all_notes(self):
        print(self)

    def __str__(self):
        final_string = "\n"
        for string in self.fretboard:
            for note in string:
                final_string += f"{note.name: <10}"
            final_string += "\n"
        return final_string