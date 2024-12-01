import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

from sound_emulator     import SoundEmulator

from chord_progression  import ChordProgression
from strumming_pattern  import StrummingPattern

class AudioGenerator:
    def __init__(self, chord_progression: ChordProgression, strumming_pattern: StrummingPattern, mode: str = 'add-synth', repeats: int = 1):

        self.samplerate = 44100
        #self.samplerate = 48000

        #sd.default.latency = ('high', 'high')
        #sd.default.clip_off = True
        #sd.default.samplerate = self.samplerate

        self.chord_progression = chord_progression
        self.strumming_pattern = strumming_pattern
        self.repeats = repeats

        # this is a dictionary where the key is the chord
        # and the item is that chord at various lengths   
        self.wave_list = {}
        if mode == 'ks':
            self.config_ks()
            self.ks_gen_wave_list()
        elif mode == 'add-synth':
            self.gen_wave_list()

    def config_ks(self):
        self.arg_dict                        = {}
        self.arg_dict['mode']                = 'one_z'
        # ks & eks
        #self.arg_dict['decay_factor']        = 0.95
        # eks
        self.arg_dict['stretching_factor']   = 0.2

        # 1_z & 2_z
        #self.arg_dict['t60']                 = duration*2
        self.arg_dict['brightness']          = 0.7

        self.arg_dict['pick_angle']          = 0.1
        self.arg_dict['pluck_position']      = 0.2
        self.arg_dict['level']               = 0.05
    
    def ks_gen_wave_list(self):
        for chord_voicing in self.chord_progression.voiced_chord_progression:
            self.wave_list[chord_voicing.name] = []
            #print(chord_voicing)
            for length in range(1,10): #length of strum sound depending on number of pauses that follow
                wave_length = self.strumming_pattern.note_time*length
                chord_waves = []
                for note in chord_voicing.note_list:
                    chord_wave = self.ks_gen_wave_from_note(note.frequency, wave_length)
                    chord_waves.append(chord_wave)
                combined_wave = self.ks_combine_waves(chord_waves)
                self.wave_list[chord_voicing.name].append(combined_wave)

    def ks_gen_wave_from_note(self, note_frequency: int, duration: float):
        self.arg_dict['decay_factor'] = 0.04*duration+0.95
        self.arg_dict['decay_factor'] = 0.02*duration+0.9725
        #self.arg_dict['decay_factor'] = 0.08*duration+0.95
        #self.arg_dict['decay_factor'] = 0.015*duration+0.983125

        self.arg_dict['t60'] = duration*5
        wave = SoundEmulator(note_frequency, duration, self.samplerate, self.arg_dict)
        return wave.output_array

    def ks_combine_waves(self, waves: list):
        final_wave = sum(waves)
        # normalize 
        final_wave = np.int16(final_wave/np.max(np.abs(final_wave)) * 32767)
        return final_wave

    def play_audio(self):
        print(self.strumming_pattern.strumming_pattern)
        to_play = []
        for _ in range(self.repeats):
            for chord_voicing in self.chord_progression.voiced_chord_progression:
                for strum_time in self.strumming_pattern.strum_length_list:
                    temp = self.wave_list[chord_voicing.name][strum_time]
                    to_play.extend(temp)
                    #time.sleep(self.strumming_pattern.note_time*0.001)
        sd.play(to_play, blocking=True)

    #################################################### Additive Synthesis functions ############

    def gen_wave_list(self):
        samples = np.arange(self.samplerate * self.strumming_pattern.note_time*9) / self.samplerate
        envelope = self.adsr_envelope(samples)

        for chord_voicing in self.chord_progression.voiced_chord_progression:
            self.wave_list[chord_voicing.name] = []
            #print(chord_voicing)
            for length in range(1,10): #length of strum sound depending on number of pauses that follow
                chord_waves = []
                for note in chord_voicing.note_list:
                    chord_wave = self.gen_wave_from_note(note.frequency, self.strumming_pattern.note_time*(length))
                    chord_waves.append(chord_wave)
                x_dim = np.arange(self.samplerate * self.strumming_pattern.note_time*(length)) / self.samplerate
                combined_wave = self.combine_waves(chord_waves, envelope[:len(chord_wave)], x_dim)
                self.wave_list[chord_voicing.name].append(combined_wave)

    def gen_wave_from_note(self, note_frequency: int, duration: float):
        modulation_strength = 0.001
        samples = np.arange(self.samplerate * duration) / self.samplerate
        wave = np.zeros(len(samples))
        modulation = np.zeros(len(samples))
        # Additive synthesis with harmonics
        #harmonic_factor =    [0.2,  1.0, 71.0, 136.0, 11.0, 20.0]
        #harmonic_frequency = [0.75, 1,   2,    3,     4,    5]
        #harmonic_factor =       [0.20, 1.00, 0.60, 71.0, 136., 11.0, 20.0, 4.50, 8.00, 5.60, 5.60, 4.50]
        #harmonic_frequency =    [0.75, 1.00, 1.25, 2.00, 3.00, 4.00, 5.00, 6.10, 7.25, 8.25, 9.25, 10.0]
        # harmonic_factor =       [0.5, 2.00, 10.0, 1.00, 1.00, 20.0, 25.0, 5.00, 1.50, 3.00, 0.50, 1.50, 0.20, 0.50]
        # harmonic_frequency =    [0.5, 0.75, 1.00, 1.25, 1.50, 2.00, 3.00, 4.00, 5.05, 6.10, 7.15, 8.25, 9.35, 10.5]
        harmonic_factor =       [1.000, 0.736, 0.362, 0.195, 0.182, 0.449, 0.341, 0.250, 0.116, 0.229] 
        harmonic_frequency =    [1.000, 2.000, 3.000, 4.000, 5.000, 6.000, 7.000, 10.00, 11.00, 12.00]




        for index, harmonic in enumerate(harmonic_frequency):
            frequency = note_frequency * harmonic
            amplitude = harmonic_factor[index] * 100  # Adjust the amplitude for each harmonic
            
            if index != 2:
                # Introduce pitch modulation using a low-frequency oscillator (LFO)
                modulation = np.sin(2 * np.pi * 5 * samples) # LFO with 5 Hz frequency
                modulated_frequency = frequency * (1 + modulation_strength * modulation)
            else:
                modulated_frequency = frequency
            
            wave += amplitude * np.sin(2 * np.pi * modulated_frequency * samples)
        
        #wave = np.int16(wave/np.max(np.abs(wave)) * 32767)

        # print(note_frequency)
        #print(note_frequency)
        #self.plot(modulation, modulated_frequency, samples)
        #self.plot(modulated_frequency, wave, samples)
        return wave

    def adsr_envelope(self, samples):
        envelope = np.zeros(len(samples))
        # Define ADSR parameters
        attack_time     = 0.001  # Attack time in seconds
        decay_time      = 0.1   # Decay time in seconds
        sustain_time    = 0.1  # Sustain time in seconds
        sustain_level   = -0.2  # Sustain level (normalized to 1)

        attack_samples  = int(attack_time * len(samples))
        decay_samples   = int(decay_time * len(samples))
        sustain_samples = int(sustain_time * len(samples))
        release_samples = len(samples) - (attack_samples + decay_samples + sustain_samples)

        # Attack phase
        envelope[:attack_samples] = np.logspace(-5, 0, attack_samples)
        # Decay phase
        envelope[attack_samples:attack_samples + decay_samples] = np.logspace(0, sustain_level, decay_samples)
        # Sustain phase
        envelope[attack_samples + decay_samples:attack_samples + decay_samples + sustain_samples] = 10**sustain_level
        # Release phase
        envelope[-release_samples:] = np.logspace(sustain_level, -2.5, release_samples)
    
        # plt.plot(samples, envelope)
        # plt.title('ADSR Envelope')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Amplitude')
        # plt.grid(True)

        # plt.show()

        return envelope

    def plot(self, wave1, wave2, x_dim):
        fig, axs = plt.subplots(3, 1, figsize=(10, 12))

        # Plot temp_wave in the first subplot
        axs[0].plot(x_dim, wave1)
        axs[0].set_title('Temp Wave')
        axs[0].set_xlabel('Time (s)')
        axs[0].set_ylabel('Amplitude')
        axs[0].grid(True)

        # Plot final_wave in the second subplot
        axs[1].plot(x_dim, wave2)
        axs[1].set_title('Final Wave')
        axs[1].set_xlabel('Time (s)')
        axs[1].set_ylabel('Amplitude')
        axs[1].grid(True)

        # Calculate FFT for temp_wave
        fft_temp_wave = np.fft.fft(wave2)
        freq_temp_wave = np.fft.fftfreq(len(wave2), d=(x_dim[1]-x_dim[0]))

        # Filter FFT data for positive frequencies up to 2000 Hz
        positive_freq_mask = (freq_temp_wave >= 0) & (freq_temp_wave <= 8000)
        freq_temp_wave_positive = freq_temp_wave[positive_freq_mask]
        fft_temp_wave_positive = fft_temp_wave[positive_freq_mask]

        # Convert FFT magnitude to dB scale
        fft_magnitude_db = 20 * np.log10(np.abs(fft_temp_wave_positive))

        # Plot FFT of temp_wave in the third subplot
        axs[2].plot(freq_temp_wave_positive, fft_magnitude_db)
        axs[2].set_title('FFT of Temp Wave (Positive Frequencies) in dB')
        axs[2].set_xlabel('Frequency (Hz)')
        axs[2].set_ylabel('Magnitude (dB)')
        axs[2].set_xscale('log')
        axs[2].set_xlim(0, 8000)  # Limit x-axis to 0-2000 Hz
        axs[2].grid(True)

        # Adjust layout
        plt.tight_layout()

        # Show the plot
        plt.show()

    def combine_waves(self, waves: list, envelope, x_dim):

        final_wave = sum(waves)
        final_wave = final_wave/len(waves)
        
        final_wave = final_wave * envelope

        final_wave = np.int16(final_wave/np.max(np.abs(final_wave)) * 32767)

        wav_wave = np.array(final_wave, dtype=np.int16)
        return wav_wave
