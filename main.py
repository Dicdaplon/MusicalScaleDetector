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
from TEST import *
from Class import *

Cscal= Audio("Gclean.wav")
Spectre, Freq=get_fft(Cscal.sample,Cscal.rate)
scores=score_for_everynote(Spectre, Freq,Cscal.rate, 10)
print("scores",scores)
scale=GetindexOfMaxNote(scores, 7)
print("scale",scale)
scalescore=compare_vector(scale, [0,2,4,5,7,9,11])
print("scalescore",scalescore)
scaleChar=compare_with_known_scale (scale)
print("scaleChar",scaleChar)
ShowFFT(Spectre, Freq)
FindScale()
TEST_compare_vector()
TEST_score_for_everynote()