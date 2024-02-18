

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

    # scales
    
    print(scales['Eb','major'])
    print(scales['D#','major'])

    print(scales['A','ionian'].notes)
    print(', '.join(scales[('A', 'ionian')].flat_notes))
    print(', '.join(scales[('A', 'ionian')].sharp_notes))

    for note in notes.chromatic_scale:
        print(scales[note,'mixolydian'])

if __name__ == "__main__":
    main()