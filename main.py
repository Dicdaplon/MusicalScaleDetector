import sklearn
import scipy
import scipy
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from scipy.io import wavfile
import scipy.io

#Internal libraries
from Function import *
from FFTfunction import *
from TEST import *
from FunctionsScaleProcessing import get_intervals_list, get_positions_in_scale_list, get_corresponding_scales
from Class import *

scale=get_max_notes("CBlues1.wav")
print("\n scale", scale)

#every_step_show("C.wav","C")


list_intervals = get_intervals_list(scale)

list_positions = get_positions_in_scale_list(list_intervals)

corresponding_scales = get_corresponding_scales(list_positions)

print('List of corresponding scales : ', corresponding_scales)



