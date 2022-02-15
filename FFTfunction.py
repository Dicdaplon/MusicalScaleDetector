import sklearn
import scipy
import scipy
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from scipy.io import wavfile
import scipy.io


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


def FFTtrunc(power, axes, StartFreq, EndFreq):
    indexStart = int(np.round(StartFreq / (axes[1])))
    indexEnd = int(np.round(EndFreq / (axes[1])))
    print(indexStart)
    print(indexEnd)
    axes = axes[indexStart:indexEnd]
    power = power[indexStart:indexEnd]
    return power, axes


def normalizeFFT(spectre, axes):
    lowfreqmean = np.mean(spectre[0:int(len(spectre) / 3)])
    highfreqmean = np.mean(spectre[int(len(spectre) * 2 / 3):len(spectre)])
    pente = (highfreqmean - lowfreqmean) / (len(spectre) - 0)
    for n in range(0, len(spectre)):
        spectre[n] = spectre[n] - (pente * n)
    return spectre, axes

def GaussianFilterFFT(power, axes, ponderation):
    WindowsSize = len(ponderation)

    truncHalfW = int(WindowsSize / 2)

    FilteredPow = np.zeros(len(power))

    for n in range(truncHalfW, len(power) - truncHalfW):  # from 0 to Pow length - windows
        windows = power[(n - truncHalfW):(n + truncHalfW + 1)]
        windows = np.multiply(windows, ponderation)
        FilteredPow[n] = np.mean(windows)

    FilteredPow = FilteredPow[truncHalfW: (len(power) - truncHalfW + 1)]

    axes = axes[truncHalfW: (len(power) - truncHalfW + 1)]

    return FilteredPow, axes