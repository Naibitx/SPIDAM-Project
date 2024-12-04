from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.io import wavfile
from scipy.signal import spectrogram
import scipy.signal
import tkinter as tk
import matplotlib.pyplot as plt
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

    if len(data.shape) > 1:
        data = data.mean(axis=1)  

    nperseg = min(256, len(data) // 2)

    frequencies, time, S_density = spectrogram(data, sample_rate, nperseg=nperseg)

    S_density[S_density == 0] = 1e-10

    fig = Figure(figsize=(6, 4))
    axis = fig.add_subplot(111)
    pmc = axis.pcolormesh(time, frequencies, 10 * np.log10(S_density), shading='gouraud')
    axis.set_title("Intensity Graph")
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Frequency (Hz)")

    fig.colorbar(pmc, ax=axis, label="Power (dB)")

    for widget in tk_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=tk_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

def plot_rt60_bands(file_path, band, tk_frame):
    sample_rate, data = wavfile.read(file_path)

    if len(data.shape) > 1:
        data = data[:, 0] 

    band_ranges = {
        "low": (100, 500),
        "mid": (500, 2000),
        "high": (2000, 8000),
        "all": None #All bands will combine low, mid, and high
    }

    if band not in band_ranges:
        raise ValueError(f"Invalid band: {band}")

    fig = Figure(figsize=(6, 4))
    axis = fig.add_subplot(111)

    if band == "all":
        #Plot all bands combined
        for band_name, (low, high) in band_ranges.items():
            if band_name != "all":
                sos = scipy.signal.butter(3, [low, high], btype='band', fs=sample_rate, output='sos')
                filtered_signal = scipy.signal.sosfilt(sos, data)
                energy = np.cumsum(filtered_signal[::-1]**2)[::-1]
                energy_to_db = 10 * np.log10(energy / np.max(energy))
                time = np.arange(len(energy_to_db)) / sample_rate
                axis.plot(time, energy_to_db, label=f"{band_name.capitalize()} Band")
    else:
        #Plot the selected band only
        low, high = band_ranges[band]
        sos = scipy.signal.butter(3, [low, high], btype='band', fs=sample_rate, output='sos')
        filtered_signal = scipy.signal.sosfilt(sos, data)
        energy = np.cumsum(filtered_signal[::-1]**2)[::-1]
        energy_to_db = 10 * np.log10(energy / np.max(energy))
        time = np.arange(len(energy_to_db)) / sample_rate
        axis.plot(time, energy_to_db, label=f"RT60 - {band.capitalize()} Band")

    axis.axhline(y=-5, color="r", linestyle="--", label="-5 dB")
    axis.axhline(y=-35, color="b", linestyle="--", label="-35 dB")
    axis.set_title(f"RT60 Graph - {band.capitalize()} Band" if band != "all" else "RT60 Graph - All Bands")
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Energy (dB)")
    axis.legend()

    #Clear the Tkinter frame and embed the plot
    for widget in tk_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=tk_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

