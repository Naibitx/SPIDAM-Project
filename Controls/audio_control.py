import os
from models.audio_model import AudioModel

class AudioControl:
    def __init__(self):
        self.audio_model = AudioModel()
    
    def load_file(self, file_path):#load audio file and perform validation
        
        try:
            self.audio_model.load_file(file_path)
            print(f"Audio file loaded: {self.audio_model.file_name}")
            return True
        except FileNotFoundError as fnfe:
            print(str(fnfe))
            return False
        except Exception as fnfe:
            print(f"Failed to load file: {str(fnfe)}")
            return False
        
    def get_file_metadata(self):#gets the metadata for the audio model
        return self.audio_model.get_metadata()

    def analyze_audio(self):

        if not self.audio_model.file_path:
            print("No audio file to analyze")
            return False
        
        '''Something here like logic for analyzing audio , etc'''

        print(f"Analyzing audio file: {self.audio_model.file_path}")
        return True
