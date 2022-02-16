import sklearn
import scipy
import scipy
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from scipy.io import wavfile
import scipy.io

from FFTfunction import *



def note_frequencies_construct():
    gamme = np.zeros(12)
    gamme[0] = 32.7  # C (Do) at 32.7 Hz

    for i in range(1, len(gamme)): #construct every note in a chromatic scale
        gamme[i] = 1.05946 * gamme[i - 1]
    return gamme


def frequence_to_index(frequence, octave, freqaxe,rate):
    freq_ind = frequence * np.power(2, octave)  # look for the selected freq and octave
    freq_ind = freq_ind + freqaxe[0]  # add a starting frequency as constant, fix for trunc function
    freq_ind = freq_ind * len(freqaxe) / rate  #transform frequence into indexes
    freq_ind=int(np.round(freq_ind))
    return freq_ind


def note_score(spectre, freq,rate, note, windows):  # return summed score for a note C,Cd,D...
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    gamme = note_frequencies_construct()  # all the normalize value, C to B (Do vers Si) in Hz

    noteindex = listscale.index(note)  # reach for the indexes of the searched note (ex Cd -> 1)
    powerscale = 0
    n = noteindex;
    np.max(spectre)
    spectre = spectre / np.max(spectre)
    for i in range(0, 6):
        freq_ind = frequence_to_index(gamme[n], i, freq,rate)
        moyennage = np.mean(spectre[freq_ind - windows:freq_ind + windows + 1]) #maybe be not usefull...
        powerscale = powerscale + moyennage
    return powerscale


def score_for_everynote(spectre, freq,rate, windows):  # return vector of summed scores for each note C,Cd,D...
    powersvector = np.zeros(12);
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    n = 0
    for note in listscale:
        powersvector[n] = note_score(spectre, freq,rate, note, 30)
        n = n + 1
    return powersvector

def compare_with_known_scale (Scalein):
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    scoremax=0
    nmax=0
    for n in range(0,len(listscale)):
        print("compare with", listscale[n])
        refscale=np.add([0,2,4,5,7,9,11],[n,n,n,n,n,n,n])
        refscale=circularyscale(refscale)
        newscore=compare_vector(Scalein,refscale)
        print("refscale", refscale, "ourscale", Scalein)
        print(" newscore",  newscore)
        if (newscore > scoremax):
            scoremax=newscore
            nmax=n

    return listscale[nmax]

def compare_vector(a, ref):  # compare 2 scale array and return a bool of identical value  BAD
    resultBool = np.zeros(len(a)) * True
    score = 0
    for n in range(0, len(a)):
        for m in range(0, len(ref)):
            if (a[n] == ref[m]):
                ponderationScaleIn = 10 / (n+1)
                if(m==(0 or 4 or 7)):   #fondamentale, tierce et quinte
                    ponderationRef=3
                else:
                    ponderationRef=0
                score = score +  ponderationScaleIn+ponderationRef
    return score


def circularyscale(scale):  # transform scale a redondant value for the >11 (13 = 1, 12 = 0 )
    for n in range(0, len(scale)):
        if (scale[n] > 11):
            scale[n] = scale[n] - 12
    scale = np.sort(scale)  #bad idea to sort everything ?
    return scale


def FindScale(our):  # return a vector of better correspondance with known scale
    Scale = [0, 2, 4, 5, 7, 9, 11]
    our = circularyscale(our)
    sumscale = np.zeros(12)
    for scaleN in range(0, 11):
        newScale = circularyscale(Scale + scaleN * np.ones(len(Scale)))
        result = BoolReturn(newScale, our)
        sumscale[scaleN] = np.sum(result)

    return sumscale



def FindScaleFromvector(ScaleScoreVector):  # return a vector of better correspondance with known scale
    SortedScaleindex = np.argsort(ScaleScoreVector)
    SortedScaleindex = SortedScaleindex[::-1]
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    return listscale[SortedScaleindex[0]]


def GetindexOfMaxNote(ChordsPowersScores, Numberofvalues):
    Sortedindexs = np.argsort(ChordsPowersScores)  # return the indexes of sorted list (ascending)
    Sortedindexs = Sortedindexs[::-1]  # indexes of the list (decreasing)
    Sortedindexs = Sortedindexs[0:Numberofvalues]
    return Sortedindexs


def GetScale(filename):
    rate, audio_data = scipy.io.wavfile.read(filename, mmap=False)
    spectre, freq = get_fft(audio_data, rate)
    # spectre,freq = fft_trunc(spectre,freq,80,800)
    for i in range(0, 1):
        spectre, freq = GaussianFilterFFT(spectre, freq, [1, 1, 1, 1, 1])

    ChordsPowersScores =score_for_everynote(spectre, freq, 5)
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    print('ChordsPowersScores', ChordsPowersScores)
    Sortedindexs = GetindexOfMaxNote(ChordsPowersScores, 7)
    print('ChordsPowersScores indexes', Sortedindexs)

    # Sortedindexs=np.sort(Sortedindexs)
    result = FindScale(Sortedindexs)
    result = FindScaleFromvector(result)

    return result



def NumberToLetter(scale):
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    letterscale = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
    for n in range(0, len(scale)):
        letterscale[n] = listscale[scale[n]]
    return letterscale


