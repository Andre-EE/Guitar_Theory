import random

class StrummingPattern:
    def __init__(self, note_value: int = None, bpm: int = 100):

        self.time_signature = (4, 4)
    
        if note_value is None:
            self.note_value = random.choices([4, 8, 16], [0.2, 0.7, 0.1])[0]
        else:
            self.note_value = note_value

        self.bpm = bpm
        self.beats_per_measure = self.time_signature[0]

        self.interval_time = 60 / bpm
        self.note_time =  self.interval_time / (self.beats_per_measure * self.note_value / 8)

        self.strumming_pattern = []
        self.strum_length_list = []

        self.gen_strumming_pattern()
        self.gen_strum_length_list()

    def gen_strumming_pattern(self):

        if self.note_value == 4:
            probability_list = [1, 0.90, 0.90, 0.90]
        elif self.note_value == 8:
            probability_list = [1, 0.25, 0.85, 0.25, 0.85, 0.25, 0.85, 0.25]
        elif self.note_value == 16:
            probability_list = [1, 0.15, 0.35, 0.15, 0.85, 0.15, 0.35, 0.15, 0.85, 0.15, 0.35, 0.15, 0.85, 0.15, 0.35, 0.15]

        for strum_probability in probability_list:
            pause_probablity = 1.0 - strum_probability
            strum_or_pause = random.choices([0, 1], [pause_probablity, strum_probability])
            self.strumming_pattern.append(strum_or_pause[0])

    def gen_strum_length_list(self):
        
        previous_strum = None
        pause_time = 0

        # after the first strum, append count if there's a strum
        # or continue to count the length of the previous strum
        # essentially count the strum + number of zeroes that follow
        for strum in self.strumming_pattern[:-1]:
            if previous_strum is not None and strum == 1:
                self.strum_length_list.append(pause_time)
                pause_time = 0
            previous_strum = strum
            pause_time = pause_time + 1

        # handle the end of the list differently to ensure that even
        # if there is no strum, the final strum length is recorded
        for strum in self.strumming_pattern[-1:]:
            if strum == 1:
                self.strum_length_list.append(pause_time)
            if strum == 0:
                self.strum_length_list.append(pause_time + 1)

    def __str__(self):
        print_string = f'\nstrumming pattern: {self.strumming_pattern} \nstrum length list: {self.strum_length_list}'
        return print_string