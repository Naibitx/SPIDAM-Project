import os
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft
from models.audio_model import AudioModel

class AudioControl:
    def __init__(self):
        self.audio_model = AudioModel()  # Initializing the AudioModel instance
    
    def load_file(self, file_path):
        """Load audio file and perform validation"""
        try:
            self.audio_model.load_file(file_path)  # Call AudioModel's load_file method
            print(f"Audio file loaded: {self.audio_model.file_name}")
            return True
        except FileNotFoundError as fnfe:
            print(str(fnfe))
            return False
        except Exception as e:
            print(f"Failed to load file: {str(e)}")
            return False

    def get_file_metadata(self):
        """Gets the metadata for the audio model"""
        return self.audio_model.get_metadata()  # Call AudioModel's get_metadata

    def analyze_audio(self):
        """Analyze audio (could be expanded with more logic)"""
        if not self.audio_model.file_path:
            print("No audio file to analyze")
            return False
        
        print(f"Analyzing audio file: {self.audio_model.file_path}")
        # Additional analysis logic could be added here
        return True
    
    def get_waveform(self):
        """Returns the waveform data (frequency and amplitude)"""
        if not self.audio_model.file_path:
            raise ValueError("No audio file loaded")
        
        sample_rate, data = wavfile.read(self.audio_model.file_path)  # Load the data using scipy
        fft_data = fft(data)  # Perform FFT on the data
        frequencies = np.fftfreq(len(data), 1 / sample_rate)  # Get the frequency data
        return frequencies[:len(frequencies) // 2], np.abs(fft_data[:len(fft_data) // 2])  # Return positive frequencies and amplitudes

