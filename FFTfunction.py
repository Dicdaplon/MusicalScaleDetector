
import numpy as np
from scipy.fft import fft



def get_fft(audio_data, rate):
    """
    Compute the fft
    Parameter:
    audio_data: audio sample array
    rate: int, sample rate in hz
    return:
    Absolute Spectre
    frequencies axes
    """

    T = (len(audio_data) - 1) * (1 / rate)
    fe = rate
    t = np.arange(start=0.0, stop=T, step=1.0 / fe)
    echantillons = audio_data
    tfd = fft(echantillons)
    N = len(echantillons)
    spectre = np.absolute(tfd) * 2 / N
    spectre = 20*np.log10(spectre)
    freq = np.arange(N) * 1.0 / T

    return spectre, freq


def get_stft(audio_data, windows_time, where_time, rate):
    """
        Compute an stft (short_time windowed fft)
        Parameter:
        audio_data: audio sample array
        rate: int, sample rate in hz
        windows_time: size of windows in s
        where_time: where in audio data ? in s
        return:
        Absolute Spectre
        frequencies axes
    """
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
    """
    Compute the summed stft all along the audio
    Parameter:
    audio_data: audio sample array
    rate: int, sample rate in hz
    windows_time: size of windows in s
    return:
    Absolute Spectre
    frequencies axes
    """
    sum_stft = 0
    windowsn = windows_time * rate
    halfwindows = int(windowsn / 2)
    Tn = (len(audio_data))
    for n in range(halfwindows, Tn - halfwindows):
        stft, freqaxes = get_stft(audio_data, windows_time, n / rate, rate)
        sum_stft = sum_stft + stft
    return sum_stft, freqaxes


########## Deprecated or not working function


def fft_trunc(spectrum, freq_axes, StartFreq, EndFreq):  # need a rewrite of the other part to work properly
    """
    trunc the spectrum and frequence axes to choosen value
    Parameter:
    spectrum: Spectral content
    freq_axes: frequencies axes
    StartFreq: start frequency in hz
    EndFreq: end frequency in hz
    return:
    Absolute Spectre
    frequencies axes
    """
    indexStart = int(np.round(StartFreq / (freq_axes[1])))
    indexEnd = int(np.round(EndFreq / (freq_axes[1])))
    print(indexStart)
    print(indexEnd)
    freq_axes = freq_axes[indexStart:indexEnd]
    spectrum = spectrum[indexStart:indexEnd]
    return spectrum, freq_axes


