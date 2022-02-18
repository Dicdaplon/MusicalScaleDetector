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


scale=get_max_notes("C.wav")
print("\n scale", scale)



#every_step_show("C.wav","C")


