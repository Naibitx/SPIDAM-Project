import tkinter as tk
from tkinter import filedialog
from controls.audio_control import AudioControl
from interface.visualization import plot_frequency, plot_waveform
class MainInterface:
    def __init__(self, root, audio_control=None):
        
        self.root = root
        self.audio_control = audio_control or AudioControl()
        self.setup_ui()

    def setup_ui(self):
        self.load_button = tk.Button(self.root, text="Load File", command=self.load_file)
        self.load_button.pack(pady=20)
        self.file_label = tk.Label(self.root, text="No file loaded")
        self.file_label.pack(pady=10)

        '''Displaying metadata'''
        self.metadata_label = tk.Label(self.root, text="", justify= "left")
        self.metadata_label.pack(pady=10)

        '''Audio Processing'''
        self.analyze_button= tk.Button(self.root, text = "Analyze Audio", command=self.analyze_audio)
        self.analyze_button.pack(pady=10)

        '''Visualization Frames'''
        self.waveform_frame = tk.Frame(self.root, bg="white", height=300)
        self.waveform_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.frequency_frame = tk.Frame(self.root, bg="white", height=300)
        self.frequency_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        '''Buttons for Visualization'''
        self.waveform_button = tk.Button(self.root, text="Show Waveform", command=self.visualize_waveform)
        self.waveform_button.pack(pady=10)

        self.frequency_button = tk.Button(self.root, text="Show Frequency ", command=self.visualize_frequency)
        self.frequency_button.pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select an audio file",
            filetypes=[("Audio Files", "*.mp3 *.aac *.wav"), ("All Files", "*.*")]
        )
        if file_path and self.audio_control.load_file(file_path): 
            self.update_file_label(file_path)
            self.display_metadata()
        else:
            self.update_file_label("No file selected")

    def update_file_label(self, file_path):
        self.file_label.config(text=f"Loaded File: {self.audio_control.audio_model.file_name}")

    def visualize_waveform(self):
        try:
            for widget in self.waveform_frame.winfo_children():
                widget.destroy() 
            if self.audio_control.audio_model.file_path:
                plot_waveform(self.audio_control.audio_model.file_path, self.waveform_frame)
            else:
                print("No audio file loaded to visualize.")
        except Exception as e:
            print(f"Error visualizing waveform: {e}")

    def visualize_frequency(self):
        try:
            for widget in self.frequency_frame.winfo_children():
                widget.destroy()  
            if self.audio_control.audio_model.file_path:
                plot_frequency(self.audio_control.audio_model.file_path, self.frequency_frame)
            else:
                print("No audio file loaded to visualize.")
        except Exception as e:
            print(f"Error visualizing frequency spectrum: {e}")

    def display_metadata(self):
        metadata = self.audio_control.get_file_metadata()
        metadata_text = "\n".join(f"{key}: {value}" for key, value in metadata.items())
        self.metadata_label.config(text=metadata_text)

    def analyze_audio(self):
        if not self.audio_control.analyze_audio():
            print("Failed to analyze audio file")

