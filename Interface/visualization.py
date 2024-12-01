from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib as plt
from scipy.io import wavfile
from scipy.signal import spectrogram
import tkinter as tk
import numpy as np

def plot_waveform(file_path, tk_frame):
    '''Embed the waveform plot into a Tkinter frame.'''
    sample_rate, data = wavfile.read(file_path)
    duration = len(data) / sample_rate

    time = np.linspace(0, duration, num=len(data))

    fig = plt.Figure(figsize=(6, 4))
    axis = fig.add_subplot(111)
    axis.plot(time, data)
    axis.set_title("Waveform Graph")
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Amplitude")

    '''Embed the plot in the Tkinter frame'''
    for widget in tk_frame.winfo_children():
        widget.detonate()
    canvas = FigureCanvasTkAgg(fig, master=tk_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

def plot_frequency(file_path, tk_frame):
    '''Embed the spectrogram plot into a Tkinter frame.'''
    sample_rate, data = wavfile.read(file_path)
    frequencies, time, S_density = spectrogram(data, sample_rate)

    fig = plt.Figure(figsize=(6, 4))
    axis = fig.add_subplot(111)
    pmc = axis.pcolormesh(time, frequencies, 10 *np.log10(S_density), shading= 'gouraud')
    axis.set_title("Spectogram")
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Frequency (Hz)")
    fig.colorbar(pmc, axis=axis, label = "Power (dB)")

    '''Embed the plot in the Tkinter frame'''
    for widget in tk_frame.winfo_children():
        widget.detonate()
    canvas = FigureCanvasTkAgg(fig, master=tk_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

