import os
from scipy.io import wavfile
from pydub import AudioSegment
from mutagen import File

class AudioModel:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.file_name= None
        self.duration = None
        self.sample_rate = None

        if file_path:
            self.load_file(file_path)
    def convert_to_wav(self, file_path): #conversion
        if not file_path.endswith(".wav"):
            audio = AudioSegment.from_file(file_path)
            wav_path=f"{os.path.splitext(file_path)[0]}.wav"
            audio.export(wav_path, format="wav")
            return wav_path
        return file_path
        
    def load_file(self, file_path):
        self.file_path = self.convert_to_wav(file_path)
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} does not exist")
        self.file_name = os.path.basename(self.file_path)

        try:
            audio_file = File(self.file_path)
            if audio_file:
                self.duration = getattr(audio_file.info, 'length', None)
                self.sample_rate = getattr(audio_file.info, 'sample_rate', None)
        except Exception as e:
            print(f"Failed to load metadata using mutagen: {e}")

            ''' Use scipy to get metadata for WAV files as a fallback'''
            if self.file_path.endswith('.wav'):
                sample_rate, data = wavfile.read(self.file_path)
                self.sample_rate = sample_rate
                self.duration = len(data) / sample_rate

    def get_metadata(self):# returns file metadata as a dictionary
        return{
            "File Name: ": self.file_name,
            "Duration (s): ": round(self.duration, 2) if self.duration else "Unknown", 
            "Sample Rate (Hz): ": self.sample_rate if self.sample_rate else "Unknown",
        }

    def reset(self):# resets model to initial state
        self.file_path = None
        self.file_name = None
        self.duration = None
        self.sample_rate = None


