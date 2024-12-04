import os
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft
from mutagen import File
import scipy.signal
from pydub import AudioSegment



'''Paths for ffmpeg and ffprobe'''
AudioSegment.converter = "/usr/local/bin/ffmpeg"
AudioSegment.ffprobe = "/usr/local/bin/ffprobe"

class AudioModel:
    def __init__(self, file_path=None):#initializing audio metadata and calculated properties attributes
        self.file_path = file_path
        self.file_name= None
        self.duration = None
        self.sample_rate = None
        self.resonant_frequency = None
        self.rt60_diff = None
        self.low_rt60 = 0.0
        self.mid_rt60 = 0.0
        self.high_rt60 = 0.0
        self.all_rt60 = 0.0

        if file_path:#file path provided, loads the audio file
            self.load_file(file_path)

    def convert_to_wav(self, file_path): #conversionaudio to wav file
        if not file_path.endswith(".wav"):# checks if file is already .wav
            audio = AudioSegment.from_file(file_path)#loads audio file
            wav_path = f"{os.path.splitext(file_path)[0]}.wav" #generates wav file path
            audio.export(wav_path, format="wav")# exports audio as wav
            return wav_path
        return file_path # returns original path if already wav

    def load_file(self, file_path): #loads audio and extracts metadata
        self.file_path = self.convert_to_wav(file_path)
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {file_path} does not exist")

        self.file_name = os.path.basename(self.file_path)# gets file name
        
        '''Handles wav files'''
        if self.file_path.endswith(".wav"):
            sample_rate, data = wavfile.read(self.file_path)
            self.sample_rate = sample_rate
            self.duration = len(data) / sample_rate #Calculates duration of audio
            #calculates resonant frequency and RT60 difference
            self.resonant_frequency = self.calculate_resonant_frequency(data, sample_rate)
            self.rt60_diff = self.calculate_rt60_diff(data, sample_rate)
        else:
            audio_file = File(self.file_path)  # extract metadata for other formats using mutagen
            if audio_file:
                self.duration = audio_file.info.length if hasattr(audio_file.info, 'length') else None
                self.sample_rate = audio_file.info.sample_rate if hasattr(audio_file.info, 'sample_rate') else None

    def calculate_resonant_frequency(self, data, sample_rate):
        #ensure that the data is in the correct format (1D array)
        if len(data.shape) > 1:
            data = data[:, 0]  #if stereo, take just one channel

        #perform FFT on the audio data
        fft_data = fft(data)
        frequencies = np.fft.fftfreq(len(fft_data), 1/sample_rate)#calculate frequency axis
        fft_magnitude = np.abs(fft_data)#get the magnitude of the FFT (absolute value)
        peak_freq_index = np.argmax(fft_magnitude) #find the index of the peak frequency
        peak_frequency = abs(frequencies[peak_freq_index])  # Get the positive frequency
        return peak_frequency
        
    def calculate_rt60_diff(self, data, sample_rate):
        if len (data.shape) > 1:
            data = data[:, 0]
        #this defines the low, mid and high bands 
        bands_filter = {
            'low': scipy.signal.butter(3, [100, 500], btype='band', fs=sample_rate, output='sos'),
            'mid': scipy.signal.butter(3, [500, 2000], btype='band', fs=sample_rate, output='sos'),
            'high': scipy.signal.butter(3, [2000, 8000], btype='band', fs=sample_rate, output='sos'),
            }
        rt60_values= {}
        for band, filter_sos in bands_filter.items():
            filtered_signals = scipy.signal.sosfilt(filter_sos, data)
            rt60_values[band]= self.estimate_rt60(filtered_signals, sample_rate)

        '''Below the RT60 Differences will be calculated'''
        self.low_rt60= rt60_values['low']
        self.mid_rt60= rt60_values['mid']
        self.high_rt60= rt60_values['high']
        self.all_rt60= np.mean(list(rt60_values.values())) 
        return self.all_rt60 - 0.5

    def estimate_rt60(self, signal, sample_rate):
        energy = np.cumsum(signal[::-1]**2)[::-1]
        energy_to_db= 10 * np.log10(energy / np.max(energy)) # converting to dB
        try: 
            t_5db = np.where(energy_to_db <= -5)[0][0]
            t_35db= np.where(energy_to_db <= -35)[0][0]
            t_diff = (t_35db - t_5db) / sample_rate # this is converting the samples to seconds
            return t_diff * 2
        except IndexError:
            return None
    
    def get_metadata(self):
        '''Returns metadata and calculated values as a dictionary '''
        return {
            "File Name: ": self.file_name,
            "Duration (s): ": round(self.duration, 2) if self.duration else "Unknown",
            "Resonant Frequency (Hz): ": round(self.resonant_frequency, 2) if self.resonant_frequency else "Unknown",
            "RT60 Difference (s): ": round(self.rt60_diff, 2) if self.rt60_diff else "Unknown"
        }


    def reset(self):
            ''' Resets model to its initial state '''
            self.file_path = None
            self.file_name = None
            self.duration = None
            self.sample_rate = None
            self.resonant_frequency = None
            self.rt60_diff = None


