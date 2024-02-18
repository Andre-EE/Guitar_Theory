from collections import deque

from helper import Helper
from helper import CollectionHelper

class Scale(Helper):
    def __init__(self, key: str, mode: str, notes: list):

        super().__init__(key)

        self._mode          = mode
        self._notes         = notes
        self._alt_notes     = []

        self._flat_notes    = []
        self._sharp_notes   = []

    @property
    def key(self):
        return self.tonic

    @property
    def alt_key(self):
        return self.alt_tonic

    @property
    def mode(self):
        return self._mode

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
        if self.alt_key is not None:
           alt_key_str  = f"({self.alt_key:<2})"
        else:
           alt_key_str  = '    '
           
        return f"{self.key: <2} {alt_key_str} {self.mode:<16}: [{notes_str:<26}]   [({alt_notes_str:<26})]"

class Scales(CollectionHelper):
    def __init__(self):

        super().__init__()
        
        self.modes =    {  
                        'ionian':               (2, 2, 1, 2, 2, 2, 1),  # major
                        'dorian':               (2, 1, 2, 2, 2, 1, 2),
                        'phrygian':             (1, 2, 2, 2, 1, 2, 2),
                        'lydian':               (2, 2, 2, 1, 2, 2, 1),
                        'mixolydian':           (2, 2, 1, 2, 2, 1, 2),  # dominant
                        'aoelian':              (2, 1, 2, 2, 1, 2, 2),  # natural / relative minor
                        'locrian':              (1, 2, 2, 1, 2, 2, 2),

                        'major':                (2, 2, 1, 2, 2, 2, 1),
                        'minor':                (2, 1, 2, 2, 1, 2, 2),

                        'major_pentatonic':     (2, 2, 3, 2, 3),        # diatonic
                        'minor_pentatonic':     (3, 2, 2, 3, 2),
                        'major_blues':          (2, 1, 1, 3, 2, 3),
                        'minor_blues':          (3, 2, 1, 1, 3, 2),
                        'harmonic_minor':       (2, 1, 2, 2, 1, 3, 1)
                        }
        
        self.generate_all_scales()

    def generate_scale(self, key: str = 'D', mode: str = 'ionian'):
        
        key_index = self.chromatic_scale.index(key)
        chromatic_scale_in_key = deque(self.chromatic_scale)
        chromatic_scale_in_key.rotate(-key_index)

        i = 0        
        generated_scale = []
        for step in self.modes[mode]:
            generated_scale.append(chromatic_scale_in_key[i]) 
            i = i + step
        return generated_scale

    def generate_all_scales(self):      
        for key in self.chromatic_scale:
            for mode in self.modes.keys():
                scale_notes = self.generate_scale(key, mode)
                current_scale = Scale(key, mode, scale_notes)
                scale_dict_key = (f"{key}", f"{mode}")
                self._instances[scale_dict_key] = current_scale
                if current_scale.alt_key is not None:
                    scale_alt_dict_key = (f"{current_scale.alt_key}", f"{mode}")
                    self._instances[scale_alt_dict_key] = current_scale
                    
    def get_scale(self, scale_dict_key: tuple):
        return self[scale_dict_key]
    
    def __getitem__(self, dict_key):
        item = self._instances.get(dict_key, None)
        item.last_access_key(dict_key)
        return item