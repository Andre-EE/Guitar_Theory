from math import exp

from helper import Helper
from helper import CollectionHelper

class Note(Helper):
    def __init__(self, name: str):

        super().__init__(name)

        self._m             = 16.3515978313 # C0 frequency
        self._b             = 0.057762265

        self._base          = None
        self._alt_base      = None

        self._octave        = None
        self._index         = None
        self._frequency     = None    

        self._fret_list     = []

    @property
    def name(self):
        return self.tonic
    @name.setter
    def name(self, value: str):
        self._base          = None
        self._alt_base      = None
        self.tonic          = value

    @property
    def alt_name(self):
        return self.alt_tonic
    
    @property
    def base(self):
        if self._base is None:
            self._base = self.tonic[:-1]
        return self._base
    
    @property
    def alt_base(self):
        if self._alt_base is None:
            self._alt_base = self.alt_tonic[:-1]
        return self._alt_base

    @property
    def octave(self):
        if self._octave is None:
            self._octave = int(self.name[-1:])
        return self._octave
    
    @property           # extentened piano index C0 to B8
    def index(self):
        if self._index is None:
            chromatic_scale_index = self.get_chromatic_scale_index()
            self._index = self.octave * 12 + chromatic_scale_index
        return self._index
    
    @property
    def frequency(self):
        if self._frequency is None:
            self._frequency = self._m * exp(self.index * self._b)
            self._frequency = int(round(self._frequency, 0))
        return self._frequency
    
    #check if I end up using this
    @property
    def fret_list(self):
        return self._fret_list
    @fret_list.setter
    def fret_list(self, value: tuple):
        if (type(value) is tuple) and (value not in self.fret_list):
            self._fret_list.append(value)
        elif type(value) is list:
            self._fret_list = value

    def __str__(self):
        if self.alt_name is not None:
           alt_name_str = f" ({self.alt_name})"
        else:
           alt_name_str = ''
        return f"{self.name}{alt_name_str}: {self.base}, {self.octave}, {self.frequency} Hz, index: {self.index}"

class Notes(CollectionHelper):
    def __init__(self):
        super().__init__()
        self.generate_all_notes()

    def generate_all_notes(self):
        for note in self.chromatic_scale:
            for octave in range(0, 9):
                note_name = f"{note}{octave}"
                current_note = Note(name=note_name)
                self._instances[note_name] = current_note
                if current_note.alt_name is not None:
                    self._instances[current_note.alt_name] = current_note

    def get_note(self, name: str):
        note = self._instances.get(name, None)
        note.last_access_key(name)
        return note
       
    def __getitem__(self, name: str):
        note = self._instances.get(name, None)
        note.last_access_key(name)
        return note

    def get_note_by_index(self, index: int):
        for note in self._instances.values():
            if note.index == index:
                return note
        return None


notes = Notes()

print(notes.get_note('Eb4'))
print(notes.get_note('D#4'))
print(notes['Eb4'])
print(notes['D#4'])
print(notes['Eb4'].flat)
print(notes['Eb4'].sharp)
print(notes['D#4'].flat)
print(notes['D#4'].sharp)

print(notes.get_note('A4'))
print(notes.get_note('B4'))
print(notes['A4'])
print(notes['B4'])
print(notes['A4'].flat)
print(notes['B4'].sharp)

print(notes.get_note('D#4').index)
print(notes.get_note('Eb4').base)
print(notes['D#4'].frequency)
print(notes['Eb4'].octave)
