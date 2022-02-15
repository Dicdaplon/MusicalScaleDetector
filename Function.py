import sklearn
import scipy
import scipy
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from scipy.io import wavfile
import scipy.io



def note_frequencies_construct():
    gamme = np.zeros(12)
    gamme[0] = 32.7  # C (Do) at 32.7 Hz

    for i in range(1, len(gamme)):
        gamme[i] = 1.05946 * gamme[i - 1]
    return gamme


def frequence_to_index(frequence, octave, freqaxe, rate):
    Freqind = frequence * np.power(2, octave)  # look for the selected freq and octave equivalent
    Freqind = Freqind + freqaxe[0]  # add starting frequency as constant, fix for trunc function
    Freqind = Freqind * len(freqaxe) / rate
    return Freqind


def NoteScore(spectre, freq, note, windows):  # return summed score for a note C,Cd,D...
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    gamme = note_frequencies_construct()  # all the normalize value, C to B (Do vers Si) in Hz

    noteindex = listscale.index(note)  # reach for the indexes of the searched note (ex Cd -> 1)
    powerscale = 0
    n = noteindex;
    spectre = spectre / max(spectre)
    for i in range(0, 6):
        Freqind = frequence_to_index(gamme[n], i, freq, rate)
        moyennage = np.mean(spectre[round(Freqind) - windows:round(Freqind) + windows + 1])
        powerscale = powerscale + moyennage
    return powerscale


def ChordsScores(spectre, freq, windows):  # return vector of summed scores for each grade C,Cd,D...
    powersvector = np.zeros(12);
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    n = 0
    for note in listscale:
        powersvector[n] = NoteScore(spectre, freq, note, 30)
        n = n + 1
    return powersvector


def BoolReturn(a, b):  # compare 2 scale array and return a bool of identical value  BAD
    resultBool = np.zeros(len(a)) * True
    for n in range(0, len(a)):
        resultBool[n] = (a[n] == b[n])
    resultBool = np.array(resultBool, int)
    return resultBool


def compare_vector(a, b):  # compare 2 scale array and return a bool of identical value  BAD
    resultBool = np.zeros(len(a)) * True
    score = 0
    for n in range(0, len(a)):
        for m in range(0, len(b)):
            if (a[n] == b[m]):
                score = score + 1
    return score


def circularyscale(scale):  # transform scale a redondant value for the >11 (13 = 1, 12 = 0 )
    for n in range(0, len(scale)):
        if (scale[n] > 11):
            scale[n] = scale[n] - 12
    scale = np.sort(scale)
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


def FindScale2(our):  # return a vector of better correspondance with known scale
    scores = np.zeros(12)
    our = circularyscale(our)
    for n in range(0, 12):
        refscale = np.add([0, 2, 4, 5, 7, 9, 11], [n, n, n, n, n, n, n])
        refscale = circularyscale(refscale)
        scores[n] = compare_vector(circularyscale(our), refscale)
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    max_scores_indexes = np.argsort(scores)
    return listscale[max_scores_indexes[0]]


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
    # spectre,freq = FFTtrunc(spectre,freq,80,800)
    for i in range(0, 1):
        spectre, freq = GaussianFilterFFT(spectre, freq, [1, 1, 1, 1, 1])

    ChordsPowersScores = ChordsScores(spectre, freq, 5)
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    print('ChordsPowersScores', ChordsPowersScores)
    Sortedindexs = GetindexOfMaxNote(ChordsPowersScores, 7)
    print('ChordsPowersScores indexes', Sortedindexs)

    # Sortedindexs=np.sort(Sortedindexs)
    result = FindScale(Sortedindexs)
    result = FindScaleFromvector(result)

    return result


def GetScale_2(filename):
    rate, audio_data = scipy.io.wavfile.read(filename, mmap=False)
    spectre, freq = get_fft(audio_data, rate)
    # spectre,freq = FFTtrunc(spectre,freq,80,800)
    for i in range(0, 2):
        spectre, freq = GaussianFilterFFT(spectre, freq, [1, 1, 1, 1, 1])

    ChordsPowersScores = ChordsScores(spectre, freq, 5)
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    print('ChordsPowersScores', ChordsPowersScores)
    Sortedindexs = GetindexOfMaxNote(ChordsPowersScores, 7)

    print('ChordsPowersScores indexes', Sortedindexs)
    result = FindScale2(Sortedindexs)
    return result


def NumberToLetter(scale):
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    letterscale = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
    for n in range(0, len(scale)):
        letterscale[n] = listscale[scale[n]]
    return letterscale


