import tkinter as tk
from customtkinter import *
from interface.main_interface import MainInterface
from controls.audio_control import AudioControl
from models.audio_model import AudioModel

def main():
    
    root = tk.Tk()
    root.title("Data Acoustic Modeling Application")
    root.geometry("1000x800")
    root.configure(bg="#002300")

    audio_control = AudioControl()

    interface = MainInterface(root, audio_control)
    audio_control.view = interface

    root.mainloop()


if __name__ == "__main__":
    main()