from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.io import wavfile
from scipy.signal import spectrogram
import tkinter as tk
import numpy as np

def plot_waveform(file_path, tk_frame):
    '''Embed the waveform plot into a Tkinter frame.'''
    sample_rate, data = wavfile.read(file_path)
    duration = len(data) / sample_rate

    time = np.linspace(0, duration, num=len(data))

    fig = Figure(figsize=(6, 4))
    axis = fig.add_subplot(111)
    axis.plot(time, data)
    axis.set_title("Waveform Graph")
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Amplitude")

    '''Embed the plot in the Tkinter frame'''
    for widget in tk_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=tk_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

def plot_frequency(file_path, tk_frame):
    '''Embed the spectrogram plot into a Tkinter frame.'''
    sample_rate, data = wavfile.read(file_path)

    # Handle stereo audio by converting to mono (average the two channels)
    if len(data.shape) > 1:
        data = data.mean(axis=1)  # Convert stereo to mono

    # Ensure nperseg is appropriate for the length of the data
    nperseg = min(256, len(data) // 2)

    # Compute the spectrogram
    frequencies, time, S_density = spectrogram(data, sample_rate, nperseg=nperseg)

    # Create the plot
    fig = Figure(figsize=(6, 4))
    axis = fig.add_subplot(111)
    pmc = axis.pcolormesh(time, frequencies, 10 * np.log10(S_density), shading='gouraud')
    axis.set_title("Spectrogram")
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Frequency (Hz)")

    # Add a colorbar
    fig.colorbar(pmc, ax=axis, label="Power (dB)")

    # Embed the plot in the Tkinter frame
    for widget in tk_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=tk_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()
