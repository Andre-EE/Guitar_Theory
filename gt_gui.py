import tkinter as tk
from tkinter import ttk
from notes import Notes
from scales import Scales
from chords import Chords
from fretboard import Fretboard

class MusicTheoryGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Theory Visualizer")
        
        self.notes = Notes()
        self.scales = Scales()
        self.chords = Chords()
        self.fretboard = Fretboard(self.notes)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scale selection
        ttk.Label(self.frame, text="Scale Key:").grid(row=0, column=0, padx=5, pady=5)
        self.scale_key = ttk.Combobox(self.frame, values=self.scales.chromatic_scale)
        self.scale_key.grid(row=0, column=1, padx=5, pady=5)
        self.scale_key.set("C")
        
        ttk.Label(self.frame, text="Scale Mode:").grid(row=0, column=2, padx=5, pady=5)
        self.scale_mode = ttk.Combobox(self.frame, values=list(self.scales.modes.keys()))
        self.scale_mode.grid(row=0, column=3, padx=5, pady=5)
        self.scale_mode.set("major")
        
        ttk.Button(self.frame, text="Show Scale", command=self.show_scale).grid(row=0, column=4, pady=10)
        
        # Chord selection
        ttk.Label(self.frame, text="Chord Root:").grid(row=1, column=0, padx=5, pady=5)
        self.chord_root = ttk.Combobox(self.frame, values=self.chords.chromatic_scale)
        self.chord_root.grid(row=1, column=1, padx=5, pady=5)
        self.chord_root.set("C")
        
        ttk.Label(self.frame, text="Chord Quality:").grid(row=1, column=2, padx=5, pady=5)
        self.chord_quality = ttk.Combobox(self.frame, values=self.chords.get_qualities())
        self.chord_quality.grid(row=1, column=3, padx=5, pady=5)
        self.chord_quality.set("major")
        
        ttk.Button(self.frame, text="Show Chord", command=self.show_chord).grid(row=1, column=4, pady=10)
        
        # Fretboard
        self.fretboard_canvas = tk.Canvas(self.frame, width=800, height=200, bg="white")
        self.fretboard_canvas.grid(row=2, column=0, columnspan=5, padx=10, pady=10)
        self.draw_fretboard()
        
        # Display area
        self.display = tk.Text(self.frame, height=3, width=50)
        self.display.grid(row=3, column=0, columnspan=5, padx=5, pady=5)
        
    def draw_fretboard(self):
        self.string_spacing = 30
        self.fret_spacing = 50
        
        # Draw strings
        for i in range(6):
            y = 20 + i * self.string_spacing
            self.fretboard_canvas.create_line(20, y, 770, y)
            
        # Draw frets
        for i in range(16):
            x = 20 + i * self.fret_spacing
            self.fretboard_canvas.create_line(x, 20, x, 170)
            
        # Add fret numbers
        for i in range(16):
            x = 20 + i * self.fret_spacing
            self.fretboard_canvas.create_text(x, 190, text=str(i))
            
        # Add open string notes
        open_notes = ['E', 'B', 'G', 'D', 'A', 'E']
        for i, note in enumerate(open_notes):
            y = 20 + i * self.string_spacing
            self.fretboard_canvas.create_text(10, y, text=note)

    def show_scale(self):
        key = self.scale_key.get()
        mode = self.scale_mode.get()
        scale = self.scales.get_scale((key, mode))
        self.display.delete(1.0, tk.END)
        self.display.insert(tk.END, str(scale))
        self.highlight_notes(scale.notes)
        
    def show_chord(self):
        root = self.chord_root.get()
        quality = self.chord_quality.get()
        chord = self.chords.get_chord((root, quality))
        self.display.delete(1.0, tk.END)
        self.display.insert(tk.END, str(chord))
        self.highlight_notes(chord.notes)
        
    def highlight_notes(self, notes):
        self.fretboard_canvas.delete("highlight")
        for string in range(6):
            for fret in range(16):
                note = self.fretboard.fretboard[string][fret].base
                if note in notes:
                    x = 20 + fret * self.fret_spacing
                    y = 20 + string * self.string_spacing
                    self.fretboard_canvas.create_oval(x-5, y-5, x+5, y+5, fill="red", tags="highlight")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicTheoryGUI(root)
    root.mainloop()