import numpy as np
import sounddevice as sd
from scipy import signal

class SoundEmulator:
    def __init__(self, note_freq, duration, samplerate, arg_dict):

        self.note_freq      = note_freq
        self.duration       = duration
        self.samplerate     = samplerate 
        self.arg_dict       = arg_dict

        self.process_arg_dict()

        self.delay_line_len = int(self.samplerate / self.note_freq)
        self.signal_len     = int(self.samplerate * self.duration)
        self.signal_array   = np.zeros(self.signal_len)
        self.output_array   = np.zeros(self.signal_len)

        self.run_filter_chain()

    def process_arg_dict(self):
        #arg_list = [mode, decay_factor, stretching_factor, t60, brightness, pick_angle, pluck_position, level]
        self.mode               = self.arg_dict.get("mode")
        self.decay_factor       = self.arg_dict.get("decay_factor")
        self.stretching_factor  = self.arg_dict.get("stretching_factor")
        self.t60                = self.arg_dict.get("t60")
        self.brightness         = self.arg_dict.get("brightness")
        self.pick_angle         = self.arg_dict.get("pick_angle")
        self.pluck_position     = self.arg_dict.get("pluck_position")
        self.level              = self.arg_dict.get("level")
        
        # Ensure decay_factor is between 0 and 1
        self.decay_factor       = np.clip(self.decay_factor, 0, 1)
        # Ensure pluck_position is between 0 and 1
        self.pluck_position     = np.clip(self.pluck_position, 0, 1)
        # TO DO add bounds for other variables


    def ks_coeff(self):
        # Loop filter
        # z^-N
        b_ks = np.zeros(self.delay_line_len + 1)
        b_ks[-1] = 1

        # 1 - H(z)z^-N
        a_ks = np.zeros(self.delay_line_len + 2)
        a_ks[0] = 1
        a_ks[-1] = -self.decay_factor*0.5
        a_ks[-2] = -self.decay_factor*0.5
        
        return b_ks, a_ks
    
    def eks_coeff(self):

        h1 = self.stretching_factor * self.decay_factor
        h0 = (1 - self.stretching_factor) * self.decay_factor

        b_eks = np.ones(1)
        a_eks = np.zeros(self.delay_line_len)
        a_eks[0] = 1
        a_eks[-1] = -h0
        a_eks[-2] = -h1

        return b_eks, a_eks

    def one_z_coeff(self):
        #P*T = (samplerate/f0)*(1/samplerate) = 1/f0
        gain_mult = 0.001**(1.0/(self.note_freq * self.t60))
        h1 = gain_mult * (0.5 * self.brightness)
        h0 = gain_mult * (1.0 - 0.5 * self.brightness)

        b_1z_damper = np.ones(1)
        a_1z_damper = np.zeros(self.delay_line_len)
        a_1z_damper[0] = 1
        a_1z_damper[-1] = -h0
        a_1z_damper[-2] = -h1

        return b_1z_damper, a_1z_damper

    def two_z_coeff(self):
        #P*T = (samplerate/f0)*(1/samplerate) = 1/f0
        gain_mult = 0.001**(1.0/(self.note_freq * self.t60))
        h1 = gain_mult * (1.0 - self.brightness) / 4.0
        h0 = gain_mult * (1.0 + self.brightness) / 2.0

        b_2z_damper = np.ones(1)
        a_2z_damper = np.zeros(self.delay_line_len + 1)
        a_2z_damper[0] = 1
        a_2z_damper[-1] = -h1
        a_2z_damper[-2] = -h0
        a_2z_damper[-3] = -h1

        return b_2z_damper, a_2z_damper

    def pick_direction(self, delayline):
    # Definition of the low pass filter, unity-dc-gain one pole : up-pick , down-pick
    # p takes two different values 0 or 0.9 depending on the pick direction        
        # H(z) = (1 - p) / (1 - p*z^-[1])

        b_pickdir = [1 - self.pick_angle]
        a_pickdir = [1, -self.pick_angle]

        y = signal.lfilter(b_pickdir, a_pickdir, delayline)
        return y

    def pick_position(self, delayline):
        #pluck_position     = β   # 1 <--- at nut ------ at bridge ---> 0
        #delay_line_length  = N
        #b = 0.9                 
        #H(z) = 1 - b*z^-(β*N)

        # Calculate the delay in samples (β*N)
        delay = int(self.pluck_position * self.delay_line_len + 0.5) #***
        
        # Create filter coefficients
        b_pickpos       = np.zeros(delay + 1)
        b_pickpos[0]    = 1
        #b_pickpos[-1]   = -self.decay_factor  # Use the energy loss parameter
        b_pickpos[-1]   = -1
        a_pickpos       = np.ones(1)
        
        #if plot_bode: show_bode_plot(filter_b, filter_a) 

        # Apply the filter
        y = signal.lfilter(b_pickpos, a_pickpos, delayline)

        return y

    def dynamic_level(self):
        level0 = self.level**(1/3)
        Lw = np.pi * self.note_freq / self.samplerate # == w * T/2

        b_dyn_lvl = np.array([Lw, Lw])
        a_dyn_lvl = np.array([1+Lw, -1+Lw])

        y = signal.lfilter(b_dyn_lvl, a_dyn_lvl, self.output_array)

        #np_samples = np.array(self.output_array)
        #return (level * level0 * np_samples) + (1.0 - level) * y
        return (self.level * level0 * self.output_array) + (1.0 - self.level) * y
    
    def run_filter_chain(self):
        
        np.random.seed(42)
        Zi = 2*np.random.rand(self.delay_line_len)-1

        Zi = self.pick_direction(Zi)
        Zi = self.pick_position(Zi)

        self.signal_array[:self.delay_line_len] = Zi

        # Generate filter coefficients
        if self.mode == 'ks':
            b, a = self.ks_coeff()
        elif self.mode == 'eks':
            b, a = self.eks_coeff()
        elif self.mode == 'one_z':    
            b, a = self.one_z_coeff()
        elif self.mode == 'two_z':  
            b, a = self.two_z_coeff()

        # Apply the filter
        self.output_array = signal.lfilter(b, a, self.signal_array)
        self.output_array = self.dynamic_level()
        #self.normalize()

    def normalize(self):
         self.output_array = np.int16(self.output_array/np.max(np.abs(self.output_array)) * 32767)

    def play_note(self):
        self.normalize()
        sd.play(self.output_array, self.samplerate)
        sd.wait()

# def main():

#     arg_dict                        = {}
#     arg_dict['mode']                = 'two_z'
#     # ks & eks
#     arg_dict['decay_factor']        = 0.99
#     # eks
#     arg_dict['stretching_factor']   = 0.8

#     # 1_z & 2_z
#     arg_dict['t60']                 = 3
#     arg_dict['brightness']          = 0.7


#     arg_dict['pick_angle']          = 0.850
#     arg_dict['pluck_position']      = 0.2
#     arg_dict['level']               = 0.1

#     note_freq       = 110
#     duration        = 2
#     sampling_freq   = 44100

#     A_test = SoundEmulator(note_freq, duration, sampling_freq, arg_dict)
#     C_test = SoundEmulator(131, duration, sampling_freq, arg_dict)
#     E_test = SoundEmulator(165, duration, sampling_freq, arg_dict)

#     A_test.output_array = A_test.output_array + C_test.output_array + E_test.output_array
#     A_test.play_note()
     
# if __name__ == "__main__":
#     main()