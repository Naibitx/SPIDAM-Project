import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from controls.audio_control import AudioControl
from interface.visualization import plot_frequency, plot_waveform, plot_rt60_bands

class MainInterface:
    def __init__(self, root, audio_control=None):
        
        self.root = root
        self.audio_control = audio_control or AudioControl()
        self.current_band = 0
        self.bands = ["Low RT60 Graph", "Mid RT60 Graph", "High RT60 Graph", "Combined RT60 Graphs"]
        self.setup_ui()

    def setup_ui(self):

        self.load_frame = tk.Frame(self.root, bg="#819381")
        self.load_frame.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        self.load_button = tk.Button(self.load_frame, text="Load File", command=self.load_file, )
        self.load_button.grid(row=0, column=0, padx=10, pady=5) 

        self.file_label = tk.Label(self.load_frame, text="No file loaded", anchor='w',  bg="#819381", fg="white")
        self.file_label.grid(row=0, column=1, padx=10, pady=5)  

        #displaying metadata above the buttons
        self.metadata_frame = tk.Frame(self.root, bg="#819381", highlightbackground="white")
        self.metadata_frame.grid(row=2, column=0, sticky='w', padx=10, pady=10)

        self.metadata_label = tk.Label(self.metadata_frame, text="", justify="left", bg="#819381", highlightbackground="white")
        self.metadata_label.grid(row=0, column=0, padx=10, pady=5)

        #frame to hold visualizations (waveform, frequency spectrum, RT60)
        self.visualization_frame = tk.Frame(self.root, bg="white", height=300)
        self.visualization_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        
        button_width= 20
        button_height= 1

        #buttons for visualization
        self.buttons_frame = tk.Frame(self.root, bg="#819381", highlightbackground="white")
        self.buttons_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.waveform_button = tk.Button(self.buttons_frame, text="Show Waveform", command=self.visualize_waveform, width=button_width, height=button_height)
        self.waveform_button.grid(row=0, column=0, padx=10)

        self.frequency_button = tk.Button(self.buttons_frame, text="Show Intensity ", command=self.visualize_frequency, width=button_width, height=button_height)
        self.frequency_button.grid(row=0, column=1, padx=10)

        #RT60 Graph button
        self.rt60_var = tk.StringVar(self.root)
        self.rt60_var.set(self.bands[0])  # Default selection (low band)
        self.rt60_dropdown = tk.OptionMenu(self.buttons_frame, self.rt60_var, *self.bands, command=self.display_rt60_graph)
        self.rt60_dropdown.config(width=button_width, height=button_height)  
        self.rt60_dropdown.grid(row=0, column=2, padx=10, pady=10)

        self.exit_button = tk.Button(self.buttons_frame, text="Exit",command=self.exit_program)
        self.exit_button.grid(row=0, column=3, padx=50)

        #ensure that grid expands to fill available space
        self.root.grid_rowconfigure(1, weight=1) 
        self.root.grid_rowconfigure(2, weight=0)  
        self.root.grid_rowconfigure(3, weight=0)  
        self.root.grid_columnconfigure(0, weight=1)

    def display_rt60_graph(self, selected_band):
        if not self.audio_control.audio_model.file_path:
            print("No audio to load")
            return

        #map dropdown values to band names
        band_mapping = {
            "Low RT60 Graph": "low",
            "Mid RT60 Graph": "mid",
            "High RT60 Graph": "high",
            "Combined RT60 Graphs": "all"
        }

        band = band_mapping.get(selected_band)
        if band is None:
            print(f"Error: Invalid band selected: {selected_band}")
            return

        #clear any existing graph in the visualization frame
        for widget in self.visualization_frame.winfo_children():
            widget.destroy()

        #plot the new RT60 graph
        try:
            plot_rt60_bands(self.audio_control.audio_model.file_path, band, self.visualization_frame)
        except ValueError as e:
            print(f"Error: {e}")
    
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

        self.metadata_label.config(text=metadata_text,font=("Courier New", 18), fg="white")
    def analyze_audio(self):
        if not self.audio_control.analyze_audio():
            print("Failed to analyze audio file")

    def exit_program(self):
        print("Exiting application...")
        self.root.destroy()
