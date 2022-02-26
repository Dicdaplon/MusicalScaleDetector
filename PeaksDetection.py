
from scipy.io import wavfile
import scipy.io

from scipy.signal import find_peaks
import matplotlib.pyplot as plt

from FFTfunction import *
from Audio import *

from scipy.misc import electrocardiogram

real_scale="Cd"
sample_number=7
type_of_sample="CleanGuitar"


file_input = get_sample_filepath(real_scale,sample_number,type_of_sample)

x = electrocardiogram()[2000:4000]
type(x)

def note_frequencies_construct(): #construct in Hz every note C to B including the # notes
    gamme = np.zeros(12)
    gamme[0] = 32.7*2  # C (Do) at 32.7 Hz

    for i in range(1, len(gamme)): #construct every note in a chromatic scale
        gamme[i] = 1.05946 * gamme[i - 1]
    return gamme


def Show_fft(Spectre,Freq,notescale,peaks): #need to implemant marker with the good note on the graph
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    scale=0
    for i in range (0,len(listscale)):
        if(listscale[i]==notescale):
            scale=i
    gamme = note_frequencies_construct()
    Biglistscale=listscale

    for n in range (0,scale):
        gamme=np.multiply(gamme,1.05946)#adapt scale frequency to selected scale
        listscale=np.concatenate([listscale,listscale])
    listscale=listscale[scale:12+scale]


    goodnote=[0,2,4,5,7,9,11]
    badnote=[1,3,6,8,10]

    Biglistscale=listscale
    Biggamme=gamme
    Biggoodnote=goodnote
    Bigbadnote=badnote

    for numberofscale in range(0,3):
        gamme=gamme*2
        Biggamme = np.concatenate([Biggamme, gamme])
        Biglistscale=np.concatenate([Biglistscale,listscale])
        goodnote=np.add(goodnote,12)
        Biggoodnote = np.concatenate([Biggoodnote,goodnote])
        badnote = np.add(badnote, 12)
        Bigbadnote = np.concatenate([Bigbadnote,badnote])

    plt.grid()
    maxfft=np.max(Spectre)
    plt.xlim(60,1000)
    for n in  Biggoodnote:
        plt.vlines(Biggamme[n], 0, maxfft, linestyles="dotted", colors="green")
        plt.text(Biggamme[n], 0, Biglistscale[n], color="green", fontsize=12)
    for n in  Bigbadnote:
        plt.vlines(Biggamme[n], 0, maxfft, linestyles="dotted", colors="red")
        plt.text(Biggamme[n], 0, Biglistscale[n], color="red", fontsize=12)


    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    fig.savefig('test2png.png', dpi=100)
    plt.xscale("log")
    plt.plot(Freq, Spectre)
    if (peaks != 0):
        plt.plot(Freq[peaks], Spectre[peaks], 'x')

    plt.plot(Freq[peaks], Spectre[peaks], 'x')
    plt.show()

filename = file_input

realscale = real_scale

listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
print("every note is associated to a number as :")
print(listscale)
print([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
print("For Example the Cmajor scale :")
print([0, 2, 4, 5, 7, 9, 11])

oursong = Audio(filename)
sample = oursong.sample
rate = oursong.rate
Spectre, Freq = get_fft(sample, rate)

Spectre = scipy.ndimage.gaussian_filter1d(Spectre, 15*2, order=0)  # smoothing the FFT

peaks, _ = find_peaks(Spectre, height=max(Spectre)/4)

"""plt.xlim(60,1000)
plt.plot(Freq,Spectre)
plt.plot(Freq[peaks], Spectre[peaks], "x")
plt.show()"""

detected_frequencies = Freq[peaks]

print('Frequencies detected in the spectre : ', detected_frequencies)

detected_notes=hz_to_note_array(detected_frequencies)
print("Peaks (Hz)", detected_frequencies)
print("Peaks (note)", detected_notes)

Show_fft(Spectre,Freq,realscale,peaks)


print("it goes here ?")