import tkinter as tk
from interface.main_interface import MainInterface
from controls.audio_control import AudioControl


def main():
    root = tk.Tk()
    root.title("Data Acoustic Modeling Application")
    root.geometry("600x400")

    audio_control = AudioControl()
    interface = MainInterface(root, audio_control)
    root.mainloop()


if __name__ == "__main__":
    main()