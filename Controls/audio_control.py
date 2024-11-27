import os

class AudioControl:
    def __init__(self):
        self.current_file = None
    
    def load_file(self, file_path):#load audio file and perform validation
        
        if os.path.exists(file_path):
            self.current_file = file_path
            print(f"Audio file loaded: {file_path}")
            return True
        else:
            print("Error: File does not exist.")
            return False
        
    def get_file_name(self):#returns the name of the current loaded file
        if self.current_file:
            return os.path.basename(self.current_file)
        else:
            return "No  file loaded"
    def analyze_audio(self):
        if not self.current_file:
            print("No audio file to analyze")
            return False
        
        print(f"Analyzing audio file: {self.current_file}")
        return True
