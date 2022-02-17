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


test=[1.0,1,1,5,1,1,1,9,1,1,2,3,5,4]

test=scipy.ndimage.gaussian_filter1d(test, 1)

print(test)
every_step_show("Cclean.wav")


