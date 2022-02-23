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
    print(indexStart)
    print(indexEnd)
    axes = axes[indexStart:indexEnd]
    power = power[indexStart:indexEnd]
    return power, axes


def normalizeFFT(spectre, axes):  # not working great for now
    lowfreqmean = np.mean(spectre[0:int(len(spectre) / 3)])
    highfreqmean = np.mean(spectre[int(len(spectre) * 2 / 3):len(spectre)])
    pente = (highfreqmean - lowfreqmean) / (len(spectre) - 0)
    for n in range(0, len(spectre)):
        spectre[n] = spectre[n] - (pente * n)
    return spectre, axes

#### POC

"""
file_input="E:\PycharmProject\JohnnyBGoode.wav"
real_scale="A#"
Audio_Obj = Audio(file_input, real_scale)
for incremant in range(0,400):
    Audio_Obj.stft(0.6,1+(incremant/10))
    Audio_Obj.smooth_fft(30)
    Audio_Obj.sum_spectrum=Audio_Obj.sum_spectrum+Audio_Obj.spectrum
    Audio_Obj.find_peaks_and_unique_from_sum()
    plt.clf()
    Audio_Obj.summed_stft_show(False)
    plt.title("Time "+ str(1+(incremant/10)) +" s, "+ str(0.4) +"s windows, increment every "+ str(1/10)+ "s ")
    max_plot_y=np.max(Audio_Obj.sum_spectrum)
    plt.text(80, max_plot_y, "Seven most powerfull notes", fontsize=20)
    plt.text(80, max_plot_y-250, Audio_Obj.unique_max_notes[0], fontsize=20)
    plt.text(100, max_plot_y-250, Audio_Obj.unique_max_notes[1], fontsize=20)
    plt.text(120, max_plot_y-250, Audio_Obj.unique_max_notes[2], fontsize=20)
    plt.text(140, max_plot_y-250, Audio_Obj.unique_max_notes[3], fontsize=20)
    plt.text(170,max_plot_y-250, Audio_Obj.unique_max_notes[4], fontsize=20)
    plt.text(210, max_plot_y - 250, Audio_Obj.unique_max_notes[5], fontsize=20)
    plt.text(240, max_plot_y - 250, Audio_Obj.unique_max_notes[6], fontsize=20)

    plt.text(300, max_plot_y-400, "Pur " +type_of_sample+ real_scale+" Sample", fontsize=20)


    plt.text(700, max_plot_y, "Real Note in scale", fontsize=20)
    plt.text(700, max_plot_y - 250, "D", fontsize=20)
    plt.text(850, max_plot_y - 250, "E", fontsize=20)
    plt.text(970, max_plot_y - 250, "F#", fontsize=20)
    plt.text(1180, max_plot_y - 250, "G", fontsize=20)
    plt.text(1300, max_plot_y - 250, "A", fontsize=20)
    plt.text(1600, max_plot_y - 250, "B", fontsize=20)
    plt.text(1800, max_plot_y - 250, "C#", fontsize=20)
    plt.pause(0.03)
""""



