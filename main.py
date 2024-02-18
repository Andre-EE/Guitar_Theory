

# Importing classes from other files
from notes import Notes
from scales import Scales

def main():
    # Initialize instances of classes from other files
    notes = Notes()
    scales = Scales()

    # # notes
    # print(notes['Eb4'])
    # print(notes.get_note('D#4'))
    # print(notes['Eb4'].flat)
    # print(notes['Eb4'].sharp)
    # print(notes['D#4'].frequency)

    # # scales
    # print(scales['Eb','major'])
    # print(scales['D#','ionian'])
    # print('')

    # print(scales['A','major_pentatonic'].notes)
    # print(', '.join(scales[('A', 'major_pentatonic')].flat_notes))
    # print('')

    # for note in notes.chromatic_scale:
    #     print(scales[note,'mixolydian'])
    # print('')

    # for mode in scales.modes:
    #     print(scales['C', mode])

    

if __name__ == "__main__":
    main()