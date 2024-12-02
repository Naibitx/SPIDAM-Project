import os
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft
from pydub import AudioSegment
from mutagen import File
from pydub import AudioSegment

AudioSegment.converter = "/usr/local/bin/ffmpeg"
AudioSegment.ffprobe = "/usr/local/bin/ffprobe"

class AudioModel:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.file_name= None
        self.duration = None
        self.sample_rate = None
        self.resonant_frequency = None
        self.rt60_diff = None

        if file_path:
            self.load_file(file_path)
    def convert_to_wav(self, file_path): #conversion
        if not file_path.endswith(".wav"):
            audio = AudioSegment.from_file(file_path)
            wav_path = f"{os.path.splitext(file_path)[0]}.wav"
            audio.export(wav_path, format="wav")
            return wav_path
        return file_path

    def load_file(self, file_path): #loads audio and extracts metadata
        self.file_path = self.convert_to_wav(file_path)
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {file_path} does not exist")

        self.file_name = os.path.basename(self.file_path)

        if self.file_path.endswith(".wav"):
            sample_rate, data = wavfile.read(self.file_path)
            self.sample_rate = sample_rate
            self.duration = len(data) / sample_rate
            self.resonant_frequency = self.calculate_resonant_frequency(data, sample_rate)
            self.rt60_diff = self.calculate_rt60_diff(data, sample_rate)
        else:
            audio_file = File(self.file_path)  # extract metadata for other formats using mutagen
            if audio_file:
                self.duration = audio_file.info.length if hasattr(audio_file.info, 'length') else None
                self.sample_rate = audio_file.info.sample_rate if hasattr(audio_file.info, 'sample_rate') else None

    def calculate_resonant_frequency(self, data, sample_rate):
        """ Calculate the resonant frequency using FFT """
        # Ensure that the data is in the correct format (1D array)
        if len(data.shape) > 1:
            data = data[:, 0]  # If stereo, take just one channel

        # Perform FFT on the audio data
        fft_data = fft(data)

        # Calculate frequency axis
        frequencies = np.fft.fftfreq(len(fft_data), 1/sample_rate)

        # Get the magnitude of the FFT (absolute value)
        fft_magnitude = np.abs(fft_data)

        # Find the index of the peak frequency
        peak_freq_index = np.argmax(fft_magnitude)
        peak_frequency = abs(frequencies[peak_freq_index])  # Get the positive frequency

        return peak_frequency
        
    def calculate_rt60_diff(self, data, sample_rate):
        """ Placeholder for RT60 calculation (simplified) """
        rt60_time = 1.5  #example RT60 time in seconds
        rt60_diff = rt60_time - 0.5  #difference from 0.5s (optimal reverb time for intelligibility)
        return rt60_diff
    
    def get_metadata(self):
        """ Returns metadata and calculated values as a dictionary """
        return {
            "File Name: ": self.file_name,
            "Duration (s): ": round(self.duration, 2) if self.duration else "Unknown",
            "Resonant Frequency (Hz): ": round(self.resonant_frequency, 2) if self.resonant_frequency else "Unknown",
            "RT60 Difference (s): ": round(self.rt60_diff, 2) if self.rt60_diff else "Unknown"
        }


    def reset(self):
            """ Resets model to its initial state """
            self.file_path = None
            self.file_name = None
            self.duration = None
            self.sample_rate = None
            self.resonant_frequency = None
            self.rt60_diff = None


