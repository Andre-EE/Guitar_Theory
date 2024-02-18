from math import exp

class CollectionHelper:
    def __init__(self):
        self._instances     = {}
        self.chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

class Helper:
    def __init__(self, tonic: str):

        self._tonic         = tonic
        self._alt_tonic     = None
        self._last_dict_key = None

        self.chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    @property
    def tonic(self):
        return self._tonic
    @tonic.setter
    def tonic(self, value: str):
        self._alt_tonic     = None
        self._tonic         = value

    @property
    def alt_tonic(self):
        if self._alt_tonic is None: 
            if self.is_flat(): 
                self._alt_tonic = self.sharp
            if self.is_sharp():
                self._alt_tonic = self.flat
        return self._alt_tonic
    
    @property
    def last_dict_key(self):
        return self._last_dict_key
    @last_dict_key.setter
    def last_dict_key(self, value: str):
        self._last_dict_key = value
        if ('b' in self._last_dict_key and self.is_sharp()) or \
            ('#' in self._last_dict_key and self.is_flat()):
            self.tonic = self.alt_tonic

    def is_sharp(self):
        return True if '#' in self.tonic else False

    def is_flat(self):
        return True if 'b' in self.tonic else False

    def get_chromatic_scale_index(self):
        chromatic_scale_index = self.chromatic_scale.index(self.tonic[:1])
        if self.is_sharp():
            chromatic_scale_index += 1
        if self.is_flat():
            chromatic_scale_index -= 1
        return chromatic_scale_index
    

