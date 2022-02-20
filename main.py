import sklearn
import scipy
import scipy
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from scipy.io import wavfile
import scipy.io
import os

#Internal libraries
from Function import *
from FFTfunction import *
from TEST import *
from Scale import Scale
from Class import *

file_input = "D.wav"

scale=get_max_notes(file_input)

print("\n scale", scale)

#every_step_show("C.wav","C")

target_folder = 'outputs/' + os.path.splitext(file_input)[0]

new_scale = Scale(scale, target_folder)

list_intervals = new_scale.get_list_intervals()

list_positions = new_scale.get_list_positions_in_scale()

list_corresponding_scales = new_scale.get_list_corresponding_scales()

list_english_notation = new_scale.get_list_english_notation()

new_scale.generate_fretboard_svg()

new_scale.save_result_to_csv()

