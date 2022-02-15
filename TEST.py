import unittest

def TEST_compare_scales():
    score = compare_scales([0, 2, 7, 5, 6], [1, 5, 6, 7, 8])
    print("TEST_compare_Scale", score)
    score = compare_scales([0, 2, 7, 5, 6], [0, 2, 7, 5, 6])
    print("TEST_compare_Scale", score)
    score = compare_scales([1, 2, 3, 4, 5], [0, 6, 7, 8, 9])
    print("TEST_compare_Scale", score)

import sklearn
import scipy
import scipy
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from scipy.io import wavfile
import scipy.io




def TEST_BoolReturn():
    result = BoolReturn([1, 2, 4, 0, 1], [1, 2, 4, 0, 1])
    groundtruth = [1, 1, 1, 1, 1]
    for i in range(0, len(result)):
        assert result[i] == groundtruth[i], "Boolreturn detect 2 identic array as different"

    result = BoolReturn([0, 2, 6, 0, 1], [1, 2, 4, 0, 1])
    groundtruth = [0, 1, 0, 1, 1]
    for i in range(0, len(result)):
        assert result[i] == groundtruth[i], "Boolreturn"


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


def TEST_GaussianFilterFFT():
    rate, audio_data = scipy.io.wavfile.read("Sinus440.wav", mmap=False)
    Pow, Axes = get_fft(audio_data, rate)
    MaxIndex = np.argsort(Pow)
    MaxIndex = MaxIndex[::-1]
    print(Axes[MaxIndex[0]])
    # ponderation=[1,1,1,2,2,3,3,4,20,4,3,3,2,2,1,1,1]
    # ponderation=[1,1,1]
    ponderation = [1, 1, 1, 1, 1]
    # ponderation=[1,1,1,1,1,1,1]
    print(len(Axes))
    print(len(Pow))
    for i in range(0, 2):
        Pow, Axes = GaussianFilterFFT(Pow, Axes, ponderation)
    MaxIndex = np.argsort(Pow)
    MaxIndex = MaxIndex[::-1]
    print(len(Axes))
    print(len(Pow))
    print(Axes[MaxIndex[0]])

