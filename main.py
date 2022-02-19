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
from FunctionsScaleProcessing import Scale
from Class import *

scale=get_max_notes("Gclean.wav")
print("\n scale", scale)

#every_step_show("C.wav","C")


new_scale = Scale(scale)

list_intervals = new_scale.get_list_intervals()

list_positions = new_scale.get_list_positions_in_scale()

list_corresponding_scales = new_scale.get_list_corresponding_scales()

list_english_notation = new_scale.get_list_english_notation()

new_scale.generate_fretboard_svg()

