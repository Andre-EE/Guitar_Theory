# Guitar_Theory
Console music theory app for guitar

## Notes Class
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
## Scales Class
Print scales:
```
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
## Chords Class
Print chords:
```
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

## Chords in Keys Class
Print chords in keys:
```
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



