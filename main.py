

# Importing classes from other files
from notes          import Notes
from scales         import Scales
from chords         import Chords
from chords_in_keys import Chords_in_Keys
from fretboard      import Fretboard
from voicings       import Voicings

def main():
    # Initialize instances of classes from other files
    notes = Notes()
    scales = Scales()
    chords = Chords()
    chords_in_keys = Chords_in_Keys()
    fretboard = Fretboard(notes)
   

    # # notes
    # print(notes['Eb4'])
    # print(notes.get_note('D#4'))
    # print(notes['Eb4'].flat)
    # print(notes['Eb4'].sharp)
    # print(notes['D#4'].frequency)
    # print('')

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
    # print('')

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

    # for quality in chords.get_qualities():
    #     print(chords['C', quality])
    # print('')

    # # chords in keys
    # print(chords_in_keys['Eb','major'])
    # print('')
    # print(chords_in_keys['D#','major_7th'])
    # print('')

    # print(chords_in_keys['A#','minor'].chords)
    # print([f"{item[0]}_{item[1]}" for item in chords_in_keys[('A#', 'minor')].flat_chords])
    # print('')

    # for key in notes.chromatic_scale:
    #     print(chords_in_keys[key, 'major'])
    #     print('')
    # print('')

    # for degree in chords_in_keys.get_degrees():
    #     print(chords_in_keys['C', degree])
    #     print('')
    

    # print(fretboard)
    # fretboard.print_all_notes()
    # fretboard.print_open_notes()
    # for note in notes.chromatic_scale:
    #     print(f"{note:<3}: {fretboard.note_directory[note]}")

    voicings = Voicings(chords, fretboard)

    for quality in chords.get_qualities():
        print(voicings[('D', quality, 'open')])

    for chord_root in notes.chromatic_scale:
        if voicings[(chord_root, 'dominant_7th','open')]: 
            print(voicings[(chord_root, 'dominant_7th','open')])

    for chord_root in notes.chromatic_scale:
        print(voicings[(chord_root, 'major','A')])

if __name__ == "__main__":
    main()