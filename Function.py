import sklearn
import scipy
import scipy
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from scipy.io import wavfile
import scipy.io

from FFTfunction import get_fft
from Class import *


def get_max_notes(filename): #usefull for full test of the method  FOR BOUBOU
    """ 
    get_max_notes computes a wav file and extract the notes
    Parameter:
    filename: wav file

    return: list of detected notes 
    """

    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    print("every note is associated to a number as :")
    print(listscale)
    print([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    print("For Example the Cmajor scale :")
    print([0,2,4,5,7,9,11])

    oursong= Audio(filename)
    sample= oursong.sample
    rate = oursong.rate
    Spectre, Freq = get_fft(sample,rate)

    Spectre = scipy.ndimage.gaussian_filter1d(Spectre, 15, order=0)  #smoothing the FFT

    print('Size of Freq' ,str(len(Freq)))
    print('This is Freq', Freq)

    print('Size of spectre', str(len(Spectre)))
    print('This is spectre', Spectre)

    print("\n Power for every note : ")
    scores = score_for_everynote(Spectre, Freq, rate, 10) #return a vector of energy detected for every notes (float)
    for n in range(0, len(listscale)):
        print(listscale[n]," ", scores[n],"     ")


    scale = GetindexOfMaxNote(scores, 5)

    print("\n note detected ", scale)
    for n in range(0, len(scale)):
        print(listscale[scale[n]])


    return scale

def note_frequencies_construct(): #construct in Hz every note C to B including the # notes
    gamme = np.zeros(12)
    gamme[0] = 65.4  # C (Do) at 32.7 Hz

    for i in range(1, len(gamme)): #construct every note in a chromatic scale
        gamme[i] = 1.05946 * gamme[i - 1]
    return gamme


def frequence_to_index(frequence, octave, freqaxe,rate):
    freq_ind = frequence * np.power(2, octave)  # look for the selected freq and octave
    freq_ind = freq_ind + freqaxe[0]  # add a starting frequency as constant, fix for trunc function
    freq_ind = freq_ind * len(freqaxe) / rate  #transform frequence into indexes
    freq_ind=int(np.round(freq_ind))
    return freq_ind

def windows_hz_to_n(hz,freqaxe): #transform a windows in hz to a number of sample n
    hz=float(hz)
    df=freqaxe[1]-freqaxe[0]
    n=hz/df
    n=int(np.round(n))
    return n


def note_score(spectre, freq, rate, note, windows):  # return summed score for a note C,Cd,D...
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    gamme = note_frequencies_construct()  # all the normalize value, C to B (Do vers Si) in Hz
    noteindex = listscale.index(note)  # reach for the indexes of the searched note (ex Cd -> 1)
    powerscale = 0
    n = noteindex
    np.max(spectre)
    spectre = spectre / np.max(spectre)
    for i in range(0, 6):
        freq_hz=gamme[n] * np.power(2, i)
        windows_hz=0.0544*freq_hz-0.0404  #regression adjustement, the windows increase with frequency
        windows=windows_hz_to_n(windows_hz, freq)
        windows= int(np.round(windows/2))
        freq_ind = frequence_to_index(gamme[n], i, freq,rate)  #need modification to doesn't take octave in parameter
        moyennage = np.mean(spectre[freq_ind - windows:freq_ind + windows + 1]) #maybe be not usefull...
        powerscale = powerscale + moyennage
    return powerscale


def score_for_everynote(spectre, freq,rate, windows):  # return vector of summed scores for each note C,Cd,D...
    powersvector = np.zeros(12);
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    n = 0
    for note in listscale:
        powersvector[n] = note_score(spectre, freq, rate, note, 30)
        n = n + 1
    return powersvector

def compare_with_known_scale (Scalein):
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    scoremax=0
    nmax=0
    for n in range(0,len(listscale)):
        refscale=np.add([0,2,4,5,7,9,11],[n,n,n,n,n,n,n])
        fundamentals=[refscale[0],refscale[2],refscale[4]]
        refscale,fundamentals=circularyscale(refscale,fundamentals)
        newscore=compare_vector(Scalein,refscale,fundamentals)
        if (newscore > scoremax):
            scoremax=newscore
            nmax=n

    return listscale[nmax]

def compare_vector(our, ref, fundamentals):  # compare 2 scale array and return a bool of identical value  BAD
    score = 0
    fundaments_found = [0, 0, 0]
    for n in range(0, len(our)):
        for m in range(0, len(ref)):
            ponderationRef = 1
            if (our[n] == ref[m]):
                if (ref[m] == fundamentals[0]):
                    fundaments_found[0]=1
                    ponderationRef = 10
                if (ref[m] == fundamentals[1]):
                    ponderationRef = 10
                    fundaments_found[1] = 1
                if (ref[m] == fundamentals[2]):
                    ponderationRef = 10
                    fundaments_found[2] = 1
                if (np.sum(fundaments_found) == 3):
                    ponderationRef = 100
                ponderationScaleIn = 10 / ((n+1)*(n+1))  #score added decrease with order (power) off note
                score = score + (10*ponderationScaleIn*ponderationRef)
    return score


def circularyscale(scale,fundamentals):  # transform scale a redondant value for the >11 (13 = 1, 12 = 0 )
    for n in range(0, len(scale)):
        if (scale[n] > 11):
            scale[n] = scale[n] - 12
    for n in range(0, len(fundamentals)):
        if (fundamentals[n] > 11):
            fundamentals[n] = fundamentals[n] - 12
    scale = np.sort(scale)  #bad idea to sort everything ?
    return scale,fundamentals


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
    Sortedindexs = GetindexOfMaxNote(ChordsPowersScores, 7)

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


def every_step_show(filename, realscale): #usefull for full test of the method
    oursong= Audio(filename)
    sample= oursong.sample
    rate = oursong.rate
    Spectre, Freq = get_fft(sample,rate)

    #for i in range(0,1):
        #Spectre, Freq=GaussianFilterFFT(Spectre,Freq, [1,1,2,2,3,3,4,4,6,4,4,3,3,2,2,1,1])

    Spectre = scipy.ndimage.gaussian_filter1d(Spectre, 15*3, order=0)


    scores = score_for_everynote(Spectre, Freq,rate, 10)
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]

    for n in range(0, len(listscale)):
        print(listscale[n]," ", scores[n],"     ")


    scale = GetindexOfMaxNote(scores, 7)
    for n in range(0, len(scale)):
        print(listscale[scale[n]])


    for n in range(0, len(listscale)):
        refscale=np.add([0,2,4,5,7,9,11],[n, n, n, n, n, n, n])
        fundamentals = [refscale[0], refscale[2], refscale[4]]
        refscale,fundamentals=circularyscale(refscale,fundamentals)
        scalescore = compare_vector(scale, refscale,fundamentals)


    Show_fft(Spectre,Freq,realscale)

    scaleChar = compare_with_known_scale(scale)
    print("\n\n  The good scale is", scaleChar)



def Show_fft(Spectre,Freq,notescale): #need to implemant marker with the good note on the graph
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
    plt.show()


