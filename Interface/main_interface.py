import tkinter as tk
from tkinter import filedialog
from controls.audio_control import AudioControl
from interface.visualization import plot_frequency, plot_waveform, plot_rt60_bands

class MainInterface:
    def __init__(self, root, audio_control=None):
        
        self.root = root
        self.audio_control = audio_control or AudioControl()
        self.current_band = 0
        self.bands = ["low", "mid", "high", "all"]
        self.setup_ui()

    def setup_ui(self):
        # Set window size and prevent resizing
        self.root.geometry("800x800")
        self.root.resizable(False, False)

        # Frame to hold Load File button and file label, placed at the top-left
        self.load_frame = tk.Frame(self.root)
        self.load_frame.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        # 'Load File' button aligned to the left inside the load_frame
        self.load_button = tk.Button(self.load_frame, text="Load File", command=self.load_file)
        self.load_button.grid(row=0, column=0, padx=10, pady=5)  # Align left in grid

        # File label aligned to the left inside the load_frame, next to the button
        self.file_label = tk.Label(self.load_frame, text="No file loaded", anchor='w')
        self.file_label.grid(row=0, column=1, padx=10, pady=5)  # Next to the button in grid

        # Displaying metadata below the file load section
        self.metadata_label = tk.Label(self.root, text="", justify="left")
        self.metadata_label.grid(row=6, column=0, sticky='w', pady=10)

        # Frame to hold visualizations (waveform, frequency spectrum, RT60)
        self.visualization_frame = tk.Frame(self.root, bg="white", height=300)
        self.visualization_frame.grid(row=2, column=0,columnspan=2, sticky='nsew', padx=10, pady=10)

        # Visualization Buttons
        self.waveform_button = tk.Button(self.root, text="Show Waveform", command=self.visualize_waveform)
        self.waveform_button.grid(row=3, column=0, padx=10, pady=10)

        self.frequency_button = tk.Button(self.root, text="Show Frequency", command=self.visualize_frequency)
        self.frequency_button.grid(row=4, column=0, padx=10, pady=10)

        # RT60 Graph button
        self.rt60_button = tk.Button(self.root, text="Show RT60 Graph", command=self.display_rt60_graph)
        self.rt60_button.grid(row=5, column=0, padx=10, pady=10)

        # RT60 Navigation buttons
        self.rt60_previous_button = tk.Button(self.root, text="<--", command=self.previous_band)
        self.rt60_previous_button.grid(row=6, column=0, pady=10, sticky='w')

        self.rt60_next_button = tk.Button(self.root, text="-->", command=self.next_band)
        self.rt60_next_button.grid(row=6, column=1, pady=10, sticky='w')
        
        # Ensure that grid expands to fill available space
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def previous_band(self):
        self.current_band = (self.current_band- 1) % len(self.bands)
        self.display_rt60_graph()
    
    def next_band(self):
        self.current_band = (self.current_band+ 1) % len(self.bands)
        self.display_rt60_graph()
    
    def display_rt60_graph(self):
        if not self.audio_control.audio_model.file_path:
            print("No audio to load")
            return
        band = self.bands[self.current_band]
        print(f"RT60 {band} Band")
        plot_rt60_bands(self.audio_control.audio_model.file_path, band, self.visualization_frame)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select an audio file",
            filetypes=[("Audio Files", "*.mp3 *.aac *.wav"), ("All Files", "*.*")]
        )
        if file_path and self.audio_control.load_file(file_path): 
            self.update_file_label(file_path)
            self.display_metadata()#display metadata immediately
        else:
            self.update_file_label("No file selected")

    def update_file_label(self, file_path):
        self.file_label.config(text=f"Loaded File: {self.audio_control.audio_model.file_name}")

    def visualize_waveform(self):
        try: 
            if self.audio_control.audio_model.file_path:
                plot_waveform(self.audio_control.audio_model.file_path, self.visualization_frame)
            else:
                print("No audio file loaded to visualize.")
        except Exception as e:
            print(f"Error visualizing waveform: {e}")

    def visualize_frequency(self):
        try:  
            if self.audio_control.audio_model.file_path:
                plot_frequency(self.audio_control.audio_model.file_path, self.visualization_frame)
            else:
                print("No audio file loaded to visualize.")
        except Exception as e:
            print(f"Error visualizing frequency spectrum: {e}")

    def display_metadata(self):
        metadata = self.audio_control.audio_model.get_metadata()

        metadata_text = "\n".join([f"{key} {value}" for key, value in metadata.items()])

        self.metadata_label.config(text=metadata_text)
    def analyze_audio(self):
        if not self.audio_control.analyze_audio():
            print("Failed to analyze audio file")

