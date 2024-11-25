import tkinter as tk
from tkinter import filedialog

class MainInterface:
    def __init__(self, root, audio_controller=None):
        
        self.root = root
        self.audio_controller = audio_controller
        self.setup_ui()

    def setup_ui(self):
        self.load_button = tk.Button(self.root, text="Load File", command=self.load_file)
        self.load_button.pack(pady=20)
        self.file_label = tk.Label(self.root, text="No file loaded")
        self.file_label.pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select an audio file",
            filetypes=[("Audio Files", "*.mp3 *.aac *.wav"), ("All Files", "*.*")]
        )
        print(f"Selected file path: {file_path}") 
        if file_path: 
            self.update_file_label(file_path)
        else:
            self.update_file_label("No file selected")

    def update_file_label(self, file_path):
        self.file_label.config(text=f"Loaded File: {file_path}")