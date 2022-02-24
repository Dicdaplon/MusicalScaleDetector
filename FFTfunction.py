import sklearn
import scipy
import scipy
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from scipy.io import wavfile
import scipy.io
from scipy.signal import find_peaks



def get_fft(audio_data, rate):  # return absolute FFT value and freqaxes
    T = (len(audio_data) - 1) * (1 / rate)
    fe = rate
    t = np.arange(start=0.0, stop=T, step=1.0 / fe)
    echantillons = audio_data
    tfd = fft(echantillons)
    N = len(echantillons)
    spectre = np.absolute(tfd) * 2 / N
    freq = np.arange(N) * 1.0 / T
    return spectre, freq


def get_stft(audio_data, windows_time, where_time, rate):  # return absolute FFT value and freqaxes
    windowsn = windows_time * rate
    wheren = np.round(where_time * rate)
    halfwindows = int(windowsn / 2)
    audio_data = audio_data[int(wheren - halfwindows):int(wheren + halfwindows + 1)]
    audio_data = np.multiply(audio_data, np.hanning(len(audio_data)))
    padding = np.zeros(2 * len(audio_data))
    audio_data = np.concatenate([padding, audio_data, padding])

    T = (len(audio_data) - 1) * (1 / rate)
    fe = rate
    t = np.arange(start=0.0, stop=T, step=1.0 / fe)
    echantillons = audio_data
    tfd = fft(echantillons)
    N = len(echantillons)
    spectre = np.absolute(tfd) * 2 / N
    freq = np.arange(N) * 1.0 / T
    return spectre, freq


def get_summed_stft(audio_data, windows_time, rate):
    sum_stft = 0
    windowsn = windows_time * rate
    halfwindows = int(windowsn / 2)
    Tn = (len(audio_data))
    for n in range(halfwindows, Tn - halfwindows):
        stft, freqaxes = get_stft(audio_data, windows_time, n / rate, rate)
        sum_stft = sum_stft + stft
    return sum_stft, freqaxes


########## Deprecated or not working function

def fft_trunc(power, axes, StartFreq, EndFreq):  # need a rewrite of the other part to work properly
    indexStart = int(np.round(StartFreq / (axes[1])))
    indexEnd = int(np.round(EndFreq / (axes[1])))
    axes = axes[indexStart:indexEnd]
    power = power[indexStart:indexEnd]
    return power, axes





