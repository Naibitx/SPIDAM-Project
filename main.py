import tkinter as tk
from Interface.main_interface import MainInterface

def main():
    root = tk.Tk()
    root.title("Data Acoustic Modeling Application")
    interface = MainInterface(root)

    root.mainloop()

if __name__ == "__main__":
    main()