from helper import Helper
from helper import CollectionHelper

class Chords_in_Key(Helper):
    def __init__(self, key: str, degree: str, chords: list):

        super().__init__(key)

        self._degree        = degree

        self._chords        = chords
        self._alt_chords    = []

        self._flat_chords   = []
        self._sharp_chords  = []

    @property
    def key(self):
        return self.tonic

    @property
    def alt_key(self):
        return self.alt_tonic

    @property
    def degree(self):
        return self._degree

    @property
    def chords(self):
        return self._chords
    @chords.setter
    def chords(self, value: list):
        self._alt_chords = []
        self._chords     = value

    @property
    def alt_chords(self):
        if len(self._alt_chords) == 0: 
            if self.is_flat():
                self._alt_chords = self.sharp_chords
            else:
                self._alt_chords = self.flat_chords
        return self._alt_chords

    @property
    def flat_chords(self):
        if len(self._flat_chords) == 0:
            for chord in self.chords:
                if self.is_sharp(chord[0]) or self.is_flat(chord[0]):
                    chromatic_scale_index = self.get_chromatic_scale_index(chord[0])
                    flat_chord = self.chromatic_scale[chromatic_scale_index + 1] + 'b'
                    self._flat_chords.append((flat_chord, chord[1]))
                else:
                    self._flat_chords.append(chord)
        return self._flat_chords

    @property
    def sharp_chords(self):
        if len(self._sharp_chords) == 0:
            for chord in self.chords:
                if self.is_sharp(chord[0]) or self.is_flat(chord[0]):
                    chromatic_scale_index = self.get_chromatic_scale_index(chord[0])
                    sharp_chord = self.chromatic_scale[chromatic_scale_index]
                    self._sharp_chords.append((sharp_chord, chord[1]))
                else:
                    self._sharp_chords.append(chord)
        return self._sharp_chords

    def last_access_key(self, value: tuple):
        if ('b' in value[0] and self.is_sharp()) or \
            ('#' in value[0] and self.is_flat()):
            self.chords = self.alt_chords
            self.tonic  = self.alt_tonic

    # def __str__(self):
    #     notes_str       = ', '.join([f"{note:<2}" for note in self.notes])
    #     alt_notes_str   = ', '.join([f"{note:<2}" for note in self.alt_notes])
    #     if self.alt_root is not None:
    #        alt_root_str  = f"({self.alt_root:<2})"
    #     else:
    #        alt_root_str  = '    '
           
    #     return f"{self.root: <2} {alt_root_str} {self.quality:<16}: [{notes_str:<14}]   [({alt_notes_str:<14})]"

    def __str__(self):
        chords_for_print = ([f"{item[0]}_{item[1]}" for item in self.chords])
        chords_str = ', '.join(chords_for_print)
        alt_chords_for_print = ([f"{item[0]}_{item[1]}" for item in self.alt_chords])
        alt_chords_str = ', '.join(alt_chords_for_print)
        key_str = f"{self.key}_{self.degree}"
        if self.alt_key is not None:
            alt_key_str = f"{self.alt_key}_{self.degree}"
        else:
            alt_key_str = ''
 
        final_string = f"key: {key_str: <19}: [{chords_str}] \n"
        final_string += f"alt: {alt_key_str: <19}: [{alt_chords_str}]"

        return final_string

class Chords_in_Keys(CollectionHelper):
    def __init__(self):

        super().__init__()

        M   = 'major'
        m   = 'minor'
        d   = 'diminished'
        M7  = 'major_7th'
        m7  = 'minor_7th'
        D7  = 'dominant_7th'
        hd  = 'half_diminished'

        self.degrees =  {  
                        'major':        (M,  m,  m,  M,  M,  m,  d ), # major
                        'minor':        (m,  d,  M,  m,  m,  M,  M ),
                        'major_7th':    (M7, m7, m7, M7, D7, m7, hd),
                        'minor_7th':    (m7, hd, M7, m7, m7, M7, D7)  # natural minor  
                        }

        self.modes =    {  
                        'major':        (2, 2, 1, 2, 2, 2, 1),
                        'minor':        (2, 1, 2, 2, 1, 2, 2)
                        }

        #for reference
        major_base = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii']
        minor_base = ['i', 'ii', 'III', 'iv', 'v', 'VI', 'VII']
        
        self.generate_all_chords_in_key()
        
    def generate_chords_in_key(self, key: str = 'C', degree = 'major'):

        chromatic_scale_in_key = self.get_chromatic_scale_in_key(key)

        generated_scale = []
        if 'major' in degree:
            scale_formula = 'major'
        else: 
            scale_formula = 'minor'

        i = 0
        for step in self.modes[scale_formula]:
            generated_scale.append(chromatic_scale_in_key[i]) 
            i = i + step

        chords_in_key = []
        for index, note in enumerate(generated_scale):
            chords_in_key.append((note, self.degrees[degree][index]))

        return chords_in_key

    def generate_all_chords_in_key(self):
        for key in self.chromatic_scale:
            for degree in self.degrees.keys():
                chords_in_key = self.generate_chords_in_key(key, degree)
                current_chords_in_key = Chords_in_Key(key = key, degree = degree, chords = chords_in_key)
                chords_in_key_dict_key = (f"{key}", f"{degree}")
                self._instances[chords_in_key_dict_key] = current_chords_in_key
                if current_chords_in_key.alt_key is not None:
                    chords_in_key_alt_dict_key = (f"{current_chords_in_key.alt_key}", f"{degree}")
                    self._instances[chords_in_key_alt_dict_key] = current_chords_in_key

    def get_degrees(self):
        return list(self.degrees.keys())

    def get_chords_in_key(self, chords_in_key_dict_key: tuple):
        return self[chords_in_key_dict_key]
    
    def __getitem__(self, dict_key: tuple):
        item = self._instances.get(dict_key, None)
        item.last_access_key(dict_key)
        return item