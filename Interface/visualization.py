import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.io import wavfile
from scipy.fft import fft
import numpy as np

def plot_waveform(file_path, tk_frame):
    '''Embed the waveform plot into a Tkinter frame.'''
    sample_rate, data = wavfile.read(file_path)
    duration = len(data) / sample_rate
    time = np.linspace(0, duration, num=len(data))

    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(time[:10000], data[:10000])
    ax.set_title("Waveform (Amplitude vs Time)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")

    '''Embed the plot in the Tkinter frame'''
    canvas = FigureCanvasTkAgg(fig, master=tk_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def plot_frequency(file_path, tk_frame):
    '''Embed the frequency plot into a Tkinter frame.'''
    sample_rate, data = wavfile.read(file_path)
    fft_data = fft(data)
    frequencies = np.fft.fftfreq(len(data), 1 / sample_rate)

    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(frequencies[:len(frequencies) // 2], np.abs(fft_data[:len(fft_data) // 2]))
    ax.set_title("Frequency Spectrum")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude")

    '''Embed the plot in the Tkinter frame'''
    canvas = FigureCanvasTkAgg(fig, master=tk_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
