

# Importing classes from other files
from notes import Notes
from scales import Scales
from chords import Chords

def main():
    # Initialize instances of classes from other files
    notes = Notes()
    scales = Scales()
    chords = Chords()

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

    # # chords
    # print(chords['Eb','major'])
    # print(chords['D#','major_7th'])
    # print('')

    # print(chords['A#','minor'].notes)
    # print(', '.join(chords[('A#', 'minor')].flat_notes))
    # print('')

    # for root in notes.chromatic_scale:
    #     print(chords[root, 'major'])
    # print('')

    # for quality in chords.qualities:
    #     print(chords['C', quality])




if __name__ == "__main__":
    main()