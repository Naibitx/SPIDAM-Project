import os
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
    
    def load_file(self, file_path):#loads audio and extracts metadata
        self.file_path = self.convert_to_wav(file_path)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist")
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)

        audio_file = File(file_path)
        if audio_file:
            self.duration = audio_file.info.length if hasattr(audio_file.info, 'length') else None
            self.sample_rate = audio_file.info.sample_rate if hasattr(audio_file.info, 'sample_rate') else None
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


