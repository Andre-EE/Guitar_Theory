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
Print all scales of a certain mode:
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
Print scales of a certain key:
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
Print all chords of a certain quality:
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
Print chords of a certain root:
```
for quality in chords.qualities:
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



