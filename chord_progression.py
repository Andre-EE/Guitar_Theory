import random

from chords         import Chords
from chords_in_keys import Chords_in_Key, Chords_in_Keys
from voicings       import Voicings

class ChordProgression:
    def __init__(self, chords_in_key: Chords_in_Key, voicings: Voicings):
        
        self.chords_in_key              = chords_in_key
        self.voicings                   = voicings
        self.numerical_progression      = []
        self.base_chord_progression     = []
        self.voiced_chord_progression   = []
        self.gen_chord_progression()
        self.gen_voiced_chord_progression()

    @classmethod
    def random(cls, chords_in_keys: Chords_in_Keys, voicings: Voicings):
        chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        key             = random.choice(chromatic_scale)
        degree          = random.choices(chords_in_keys.get_degrees(), [0.5, 0.3, 0.1, 0.1])[0]
        chords_in_key   = chords_in_keys[key, degree]
        return cls(chords_in_key, voicings)

    @classmethod
    def from_chords_in_key(cls, chords_in_key: Chords_in_Key, voicings: Voicings):
        return cls(chords_in_key, voicings)

    def gen_chord_progression(self):
        i = 0
        current_chord = None
        if self.chords_in_key.degree in ('major', 'major_7th'):
            progression_function = self.major_chord_progression_state_machine
        elif self.chords_in_key.degree in ('minor', 'minor_7th'): 
            progression_function = self.minor_chord_progression_state_machine

        while i < 4: # generates a 4 chord progression
            current_chord = progression_function(current_chord)
            self.numerical_progression.append(current_chord)
            self.base_chord_progression.append(self.chords_in_key.chords[current_chord - 1])
            i = i + 1

    def major_chord_progression_state_machine(self, current_chord):
        if current_chord == None:
            return 1
        elif current_chord == 1:
            options     = [ 5,      7,      4,      6,      3   ]
            probablity  = [ 0.24,   0.04,   0.24,   0.24,   0.24]
            return random.choices(options, probablity)[0]
        elif current_chord == 2:
            options     = [ 5,      7,      1   ]
            probablity  = [ 0.48,   0.04,   0.48]
            return random.choices(options, probablity)[0]
        elif current_chord == 3:
            options     = [ 6,      2   ]
            probablity  = [ 0.50,   0.50]
            return random.choices(options, probablity)[0]
        elif current_chord == 4:
            return 2
        elif current_chord in (5, 7):
            options     = [ 1,      6   ]
            probablity  = [ 0.50,   0.50]
            return random.choices(options, probablity)[0]    
        elif current_chord == 6:
            return 4   

    def minor_chord_progression_state_machine(self, current_chord):
        if current_chord == None:
            return 1
        elif current_chord == 1:
            options     = [ 5,      4,      6,      3,      7   ]
            probablity  = [ 0.24,   0.04,   0.24,   0.24,   0.24]
            return random.choices(options, probablity)[0]
        elif current_chord == 2:
            options     = [ 5,      1   ]
            probablity  = [ 0.50,   0.50]
            return random.choices(options, probablity)[0]
        elif current_chord == 3:
            options     = [ 6,      7,      4   ]
            probablity  = [ 0.48,   0.48,   0.04]
            return random.choices(options, probablity)[0]
        elif current_chord == 4:
            return 2
        elif current_chord == 5:
            options     = [ 1,      6   ]
            probablity  = [ 0.50,   0.50]
            return random.choices(options, probablity)[0]        
        elif current_chord == 6:
            options     = [ 4,      3,      7   ]
            probablity  = [ 0.04,   0.48,   0.48]
            return random.choices(options, probablity)[0]
        elif current_chord == 7:
            options     = [ 3,      6   ]
            probablity  = [ 0.50,   0.50]
            return random.choices(options, probablity)[0]
    
    def gen_voiced_chord_progression(self):

        for chord_order, chord in enumerate(self.base_chord_progression):
            chord_voicing_names = self.voicings.get_list_of_voicing_names_for_chord(chord)
            if chord_order == 0:
                random_index = random.choice(range(len(chord_voicing_names)))
                first_chord_voicing = self.voicings[chord_voicing_names[random_index]]
                self.voiced_chord_progression.append(first_chord_voicing)
            else:
                chord_voicing_name = min(chord_voicing_names, key = lambda voicing_name:
                                    abs(self.voicings[voicing_name].low_fret - first_chord_voicing.low_fret))
                
                chord_voicing = self.voicings[chord_voicing_name]
                self.voiced_chord_progression.append(chord_voicing)


    def __str__(self):
        print_string = '\n'
        chord_list = []
        for voicing in self.voiced_chord_progression:
            chord_list.append(voicing.name)
            print_string += str(voicing)
        print_string += '\n'
        for item in list(zip(self.numerical_progression, chord_list)):
            print_string += f"{str(item[0]) + ':':<3} {item[1][0] + '_'+item[1][1] + ';':<16} {item[1][2]}-shape \n"

        return print_string
            