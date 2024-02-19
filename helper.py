class CollectionHelper:
    def __init__(self):
        self._instances     = {}

        self.chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

class Helper:
    def __init__(self, tonic: str):

        self._tonic         = tonic
        self._alt_tonic     = None
        
        self._flat          = None
        self._sharp         = None

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
    def flat(self):
        if self._flat is None:
            if self.is_flat() or self.is_sharp():
                chromatic_scale_index = self.get_chromatic_scale_index()
                self._flat = self.chromatic_scale[chromatic_scale_index + 1] + 'b' + self.tonic[2:]
        return self._flat

    @property
    def sharp(self):
        if self._sharp is None:
            if self.is_flat() or self.is_sharp():
                chromatic_scale_index = self.get_chromatic_scale_index()
                self._sharp = self.chromatic_scale[chromatic_scale_index] + self.tonic[2:]
        return self._sharp 

    def is_sharp(self, note: str = None):
        if note is None:
            note = self.tonic
        return True if '#' in note else False

    def is_flat(self, note: str = None):
        if note is None:
            note = self.tonic
        return True if 'b' in note else False


    def get_chromatic_scale_index(self, note = None):
        if note is None:
            note = self.tonic
        chromatic_scale_index = self.chromatic_scale.index(note[0]) #self.tonic[:1]
        if self.is_sharp(note):
            chromatic_scale_index += 1
        if self.is_flat(note):
            chromatic_scale_index -= 1
        return chromatic_scale_index


    def last_access_key(self, value: str):
        if ('b' in value and self.is_sharp()) or \
            ('#' in value and self.is_flat()):
            self.tonic = self.alt_tonic
