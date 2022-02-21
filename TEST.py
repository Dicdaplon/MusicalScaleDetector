import unittest
import sklearn
import scipy
import scipy
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from scipy.io import wavfile
import scipy.io


from Function import *
from FFTfunction import *
from Class import *



def TEST_score_for_everynote():

    rate, sample= scipy.io.wavfile.read("PerfectSequentialCscale.wav", mmap=False)
    Spectre,Freq=get_fft(sample, rate)
    scores=score_for_everynote(Spectre, Freq,rate, 10)
    indexofmax=np.argsort(scores)
    groundtruth=[0,2,4,5,7,9,11]

    print(groundtruth)
    print(indexofmax)
    for i in range(0,len(indexofmax)):
        assert groundtruth[i] == indexofmax[i]

def TEST_compare_vector():
    score1 = compare_vector([0, 2, 7, 5, 6], [0, 2, 7, 5, 6])
    score2 = compare_vector([0, 2, 7, 5, 6], [0, 1, 3, 5, 6])
    score3 = compare_vector([0, 2, 7, 5, 6], [1, 3, 4, 8, 9])
    assert score1>score2, "perfect scale identification return a worst score than an Partially good"
    assert score2 >score3, "Partially good scale identification return a worst score than an bad one"



def TEST_circularyscale():
    result = circularyscale([0, 2, 4, 5, 7, 9, 11])
    groundtruth = [0, 2, 4, 5, 7, 9, 11]
    for i in range(0, len(result)):
        assert result[i] == groundtruth[i], "Circularyscale is not suppose to change anything here"

    result = circularyscale([1, 4, 8, 12, 2, 17, 3])
    groundtruth = [0, 1, 2, 3, 4, 5, 8]
    for i in range(0, len(result)):
        assert result[i] == groundtruth[i], "Circularyscale error"


def TEST_FindScale():
    test = [0, 2, 4, 5, 7, 9, 11]
    groundtruth = 0
    predict = FindScale(test)
    SortedScaleindex = np.argsort(predict)
    SortedScaleindex = SortedScaleindex[::-1]
    assert SortedScaleindex[0] == 0


def TEST_FFTtrunc():
    rate, audio_data = scipy.io.wavfile.read("C.wav", mmap=False)
    Pow, Axes = get_fft(audio_data, rate)
    Pow, Axes = FFTtrunc(Pow, Axes, 200, 600)
    assert np.round(Axes[0]) == 200, "bad axes start in trunc function"
    assert np.round(Axes[len(Axes) - 1]) == 600, "bad axes end in trunc function"
    assert len(Pow) == len(Axes), "Different lenght Power and FreqAxes after trunc function"


