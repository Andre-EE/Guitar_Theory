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
