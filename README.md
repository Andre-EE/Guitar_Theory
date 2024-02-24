# Guitar_Theory
Console music theory app for guitar

## Notes Class
<details>
<summary>Get information on musical notes</summary>

```
notes = Notes()
print(notes['Eb4'])
print(notes.get_note('D#4'))
print(notes['Eb4'].flat)
print(notes['Eb4'].sharp)
print(notes['D#4'].frequency)
```
Result:
```
Eb4 (D#4): Eb, 4, 311 Hz, index: 51
D#4 (Eb4): D#, 4, 311 Hz, index: 51
Eb4
D#4
311
```
</details>

## Scales Class
<details>
<summary>Generate and print scales</summary>


Print scales:
```
scales = Scales()
print(scales['Eb','major'])
print(scales['D#','ionian'])

print(scales['A','major_pentatonic'].notes)
print(', '.join(scales[('A', 'major_pentatonic')].flat_notes))
```
Result:
```
Eb (D#) major           : [Eb, F , G , Ab, Bb, C , D ]   [(D#, F , G , G#, A#, C , D )]
D# (Eb) ionian          : [D#, F , G , G#, A#, C , D ]   [(Eb, F , G , Ab, Bb, C , D )]

['A', 'B', 'C#', 'E', 'F#']
A, B, Db, E, Gb
```
Print all scales of a specific mode:
```
for note in notes.chromatic_scale:
    print(scales[note,'mixolydian'])
```
Result:
```
C       mixolydian      : [C , D , E , F , G , A , A#]   [(C , D , E , F , G , A , Bb)]
C# (Db) mixolydian      : [C#, D#, F , F#, G#, A#, B ]   [(Db, Eb, F , Gb, Ab, Bb, B )]
D       mixolydian      : [D , E , F#, G , A , B , C ]   [(D , E , Gb, G , A , B , C )]
# etc...
```
Print scales of a specific key:
```
for mode in scales.modes:
    print(scales['C', mode])
```
Result:
```
C       ionian          : [C , D , E , F , G , A , B ]   [(C , D , E , F , G , A , B )]
C       dorian          : [C , D , D#, F , G , A , A#]   [(C , D , Eb, F , G , A , Bb)]
# etc...
C       major_pentatonic: [C , D , E , G , A         ]   [(C , D , E , G , A         )]
C       minor_pentatonic: [C , D#, F , G , A#        ]   [(C , Eb, F , G , Bb        )]
C       major_blues     : [C , D , D#, E , G , A     ]   [(C , D , Eb, E , G , A     )]
# etc...
```
</details>

## Chords Class

<details>
<summary>Generate and print chords</summary>


Print chords:
```
chords = Chords()
print(chords['Eb','major'])
print(chords['D#','major_7th'])

print(chords['A#','minor'].notes)
print(', '.join(chords[('A#', 'minor')].flat_notes))
```
Result:
```
Eb (D#) major           : [Eb, G , Bb    ]   [(D#, G , A#    )]
D# (Eb) major_7th       : [D#, G , A#, D ]   [(Eb, G , Bb, D )]

['A#', 'C#', 'F']
Bb, Db, F
```
Print all chords of a specific quality:
```
for root in notes.chromatic_scale:
    print(chords[root, 'major'])
```
Result:
```
C       major           : [C , E , G     ]   [(C , E , G     )]
C# (Db) major           : [C#, F , G#    ]   [(Db, F , Ab    )]
D       major           : [D , F#, A     ]   [(D , Gb, A     )]
# etc...
```
Print chords of a specific root:
```
for quality in chords.get_qualities():
    print(chords['C', quality])
```
Result:
```
C       major           : [C , E , G     ]   [(C , E , G     )]
C       minor           : [C , D#, G     ]   [(C , Eb, G     )]
# etc...
C       minor_7th       : [C , D#, G , A#]   [(C , Eb, G , Bb)]
C       dominant_7th    : [C , E , G , A#]   [(C , E , G , Bb)]
C       sus2            : [C , D , G     ]   [(C , D , G     )]
# etc...
```
</details>

## Chords in Keys Class

<details>
<summary>Generate and print chords in keys</summary>


Print chords in keys:
```
chords_in_keys = Chords_in_Keys()
print(chords_in_keys['Eb','major'])
print(chords_in_keys['D#','major_7th'])

print(chords_in_keys['A#','minor'].chords)
print([f"{item[0]}_{item[1]}" for item in chords_in_keys[('A#', 'minor')].flat_chords])
```
Result:
```
key: Eb_major           : [Eb_major, F_minor, G_minor, Ab_major, Bb_major, C_minor, D_diminished] 
alt: D#_major           : [D#_major, F_minor, G_minor, G#_major, A#_major, C_minor, D_diminished]

key: D#_major_7th       : [D#_major_7th, F_minor_7th, G_minor_7th, G#_major_7th, A#_dominant_7th, C_minor_7th, D_half_diminished]
alt: Eb_major_7th       : [Eb_major_7th, F_minor_7th, G_minor_7th, Ab_major_7th, Bb_dominant_7th, C_minor_7th, D_half_diminished]

[('A#', 'minor'), ('C', 'diminished'), ('C#', 'major'), ('D#', 'minor'), ('F', 'minor'), ('F#', 'major'), ('G#', 'major')]
['Bb_minor', 'C_diminished', 'Db_major', 'Eb_minor', 'F_minor', 'Gb_major', 'Ab_major']
```
Print all chords in keys of a specific degree:
```
for key in notes.chromatic_scale:
    print(chords_in_keys[key, 'major'])
```
Result:
```
key: C_major            : [C_major, D_minor, E_minor, F_major, G_major, A_minor, B_diminished]
alt:                    : [C_major, D_minor, E_minor, F_major, G_major, A_minor, B_diminished]

key: C#_major           : [C#_major, D#_minor, F_minor, F#_major, G#_major, A#_minor, C_diminished]
alt: Db_major           : [Db_major, Eb_minor, F_minor, Gb_major, Ab_major, Bb_minor, C_diminished]

key: D_major            : [D_major, E_minor, F#_minor, G_major, A_major, B_minor, C#_diminished]
alt:                    : [D_major, E_minor, Gb_minor, G_major, A_major, B_minor, Db_diminished]
# etc...
```
Print chords in keys of a specific key:
```
for degree in chords_in_keys.get_degrees():
    print(chords_in_keys['C', degree])
```
Result:
```
key: C_major            : [C_major, D_minor, E_minor, F_major, G_major, A_minor, B_diminished]
alt:                    : [C_major, D_minor, E_minor, F_major, G_major, A_minor, B_diminished]

key: C_minor            : [C_minor, D_diminished, D#_major, F_minor, G_minor, G#_major, A#_major]
alt:                    : [C_minor, D_diminished, Eb_major, F_minor, G_minor, Ab_major, Bb_major]

key: C_major_7th        : [C_major_7th, D_minor_7th, E_minor_7th, F_major_7th, G_dominant_7th, A_minor_7th, B_half_diminished]
alt:                    : [C_major_7th, D_minor_7th, E_minor_7th, F_major_7th, G_dominant_7th, A_minor_7th, B_half_diminished]

key: C_minor_7th        : [C_minor_7th, D_half_diminished, D#_major_7th, F_minor_7th, G_minor_7th, G#_major_7th, A#_dominant_7th]
alt:                    : [C_minor_7th, D_half_diminished, Eb_major_7th, F_minor_7th, G_minor_7th, Ab_major_7th, Bb_dominant_7th]
```
</details>

## Fretboard Class

<details>
<summary>Generate fretboard notes</summary>


Print fretboard:

```
fretboard = Fretboard(notes)
print(fretboard)

fretboard.print_all_notes()
```
Result:
```
E4        F4        F#4       G4        G#4       A4        A#4       B4        C5        C#5       D5        D#5       E5        F5        F#5
B3        C4        C#4       D4        D#4       E4        F4        F#4       G4        G#4       A4        A#4       B4        C5        C#5
G3        G#3       A3        A#3       B3        C4        C#4       D4        D#4       E4        F4        F#4       G4        G#4       A4
D3        D#3       E3        F3        F#3       G3        G#3       A3        A#3       B3        C4        C#4       D4        D#4       E4
A2        A#2       B2        C3        C#3       D3        D#3       E3        F3        F#3       G3        G#3       A3        A#3       B3
E2        F2        F#2       G2        G#2       A2        A#2       B2        C3        C#3       D3        D#3       E3        F3        F#3
```

Print open chord notes only:
```
fretboard.print_open_notes()
```
Result:
```
E4        F4        F#4       G4
B3        C4        C#4       D4
G3        G#3       A3        A#3
D3        D#3       E3        F3
A2        A#2       B2        C3
E2        F2        F#2       G2
```

Get (string, fret) locations for notes:
```
for note in notes.chromatic_scale:
    print(f"{note:<3}: {fretboard.note_directory[note]}")
```

Result
```
C  : [(0, 8), (1, 1), (1, 13), (2, 5), (3, 10), (4, 3), (5, 8)]
C# : [(0, 9), (1, 2), (1, 14), (2, 6), (3, 11), (4, 4), (5, 9)]
D  : [(0, 10), (1, 3), (2, 7), (3, 0), (3, 12), (4, 5), (5, 10)]
# etc...
```

</details>

## Voicings Class

<details>
<summary>Voice chords on the fretboard</summary>


Print voiced chords of with a specific root:
```
voicings = Voicings(chords, fretboard)

for quality in chords.get_qualities():
    print(voicings[('D', quality, 'open')])
```
Result:
```
D_major: 

--    |   --        F#4       --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        D4        --        --        --        --        --        --        --        --        --        --
--    |   --        A3        --        --        --        --        --        --        --        --        --        --        --
D3    |   --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12

D_minor:

--    |   F4        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        D4        --        --        --        --        --        --        --        --        --        --
--    |   --        A3        --        --        --        --        --        --        --        --        --        --        --
D3    |   --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12

D_major_7th:

--    |   --        F#4       --        --        --        --        --        --        --        --        --        --        --
--    |   --        C#4       --        --        --        --        --        --        --        --        --        --        --
--    |   --        A3        --        --        --        --        --        --        --        --        --        --        --
D3    |   --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12

D_minor_7th:

--    |   F4        --        --        --        --        --        --        --        --        --        --        --        --
--    |   C4        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        A3        --        --        --        --        --        --        --        --        --        --        --
D3    |   --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12

#etc 
```

Print voiced chords of a specific quality:
```
for chord_root in notes.chromatic_scale:
    if voicings[(chord_root, 'dominant_7th','open')]: 
        print(voicings[(chord_root, 'dominant_7th','open')])
```
Result:
```
C_dominant_7th:

E4    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   C4        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        A#3       --        --        --        --        --        --        --        --        --        --        --
--    |   --        E3        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        C3        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12

D_dominant_7th:

--    |   --        F#4       --        --        --        --        --        --        --        --        --        --        --        --
--    |   C4        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        A3        --        --        --        --        --        --        --        --        --        --        --        --
D3    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12

E_dominant_7th:

E4    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
B3    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   G#3       --        --        --        --        --        --        --        --        --        --        --        --        --
D3    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        B2        --        --        --        --        --        --        --        --        --        --        --        --
E2    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12

G_dominant_7th:

--    |   F4        --        --        --        --        --        --        --        --        --        --        --        --        --
B3    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
G3    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
D3    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        B2        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        G2        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12

#etc
```

Print voiced chords of a specific CAGED shape:
```
for chord_root in notes.chromatic_scale:
    print(voicings[(chord_root, 'major','A')])
```
Result:
```
C_major:

--    |   --        --        G4        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        E4        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        C4        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        G3        --        --        --        --        --        --        --        --        --
--    |   --        --        C3        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12

C#_major:

--    |   --        --        --        G#4       --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        F4        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        C#4       --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        G#3       --        --        --        --        --        --        --        --
--    |   --        --        --        C#3       --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12

D_major:

--    |   --        --        --        --        A4        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        F#4       --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        D4        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        A3        --        --        --        --        --        --        --
--    |   --        --        --        --        D3        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12

#etc

```
</details>

## Chord Progression Class

<details>
<summary>Generate chord progressions</summary>


Print progression with randomized keys, chords, and chord shapes. 
Shapes are kept near each other on the fretboard. 
G-shape and Cminor shapes are avoided.

```
random_chord_progression = ChordProgression.random(chords_in_keys, voicings)
print(random_chord_progression)
```
Result:
```

F_major:

--    |   F4        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   C4        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        A3        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        F3        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        C3        --        --        --        --        --        --        --        --        --        --        --
--    |   F2        --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12
D_minor:

--    |   F4        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        D4        --        --        --        --        --        --        --        --        --        --        --
--    |   --        A3        --        --        --        --        --        --        --        --        --        --        --        --
D3    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12
A#_major:

--    |   F4        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        D4        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        A#3       --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        F3        --        --        --        --        --        --        --        --        --        --        --
--    |   A#2       --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12
G_minor:

--    |   --        --        G4        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        D4        --        --        --        --        --        --        --        --        --        --        --
G3    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
D3    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   A#2       --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        G2        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12

1:  F_major;         E-shape
6:  D_minor;         open-shape
4:  A#_major;        A-shape
2:  G_minor;         open-shape
```

You can also generate a random progression from a specific key:

```
chord_progression = ChordProgression.from_chords_in_key(chords_in_keys['A','minor'], voicings)
print(chord_progression)
```

```
A_minor:

E4    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   C4        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        A3        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        E3        --        --        --        --        --        --        --        --        --        --        --        --
A2    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12
F_major:

--    |   F4        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   C4        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        A3        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        F3        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        C3        --        --        --        --        --        --        --        --        --        --        --
--    |   F2        --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12
C_major:

E4    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   C4        --        --        --        --        --        --        --        --        --        --        --        --        --
G3    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        E3        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        C3        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12
G_major:

--    |   --        --        G4        --        --        --        --        --        --        --        --        --        --        --
B3    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
G3    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
D3    |   --        --        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        B2        --        --        --        --        --        --        --        --        --        --        --        --
--    |   --        --        G2        --        --        --        --        --        --        --        --        --        --        --
                              3                   5                   7                   9                             12

1:  A_minor;         open-shape
6:  F_major;         E-shape
3:  C_major;         open-shape
7:  G_major;         open-shape
```


</details>

## Strumming Pattern Class

<details>
<summary>Generate strumming patterns</summary>


Print a strumming pattern with quarter, eigth, or sixteenth notes and specific beats per minute.
Starting out with only (4,4) time signature support

```
random_strumming_pattern = StrummingPattern()
print(random_strumming_pattern)

strumming_pattern = StrummingPattern(16, 120)
print(strumming_pattern)
```
Result:
```
strumming pattern: [1, 0, 1, 0, 1, 0, 1, 0]
strum length list: [2, 2, 2, 2]

strumming pattern: [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0]
strum length list: [2, 2, 4, 2, 1, 1, 1, 1, 2]
```
</details>
