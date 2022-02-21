"""""  Lot of circular import error, i'm actually trying to clean it but in conserve here all original import for now
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
import unittest

#Internal libraries
from GenerateData import *
from Function import *
from FFTfunction import *
from TEST import *
from Scale import Scale
from Class import *
#from PeaksDetection import x
"""

from Class import *


#choose your sample here
real_scale="C"
sample_number=7
type_of_sample="CleanGuitar"


file_input = get_sample_filepath(real_scale,sample_number,type_of_sample)

Audio_Obj = Audio(file_input,real_scale)
print(Audio_Obj.sample)
Audio_Obj.fft()
Audio_Obj.fft_show()
Audio_Obj.smooth_fft(30)
Audio_Obj.fft_show()
print(Audio_Obj.spectrum)
Audio_Obj.find_peaks()
print(Audio_Obj.peaks_value)
print(Audio_Obj.peaks_hz)
print(Audio_Obj.peaks_notes)



"""""
predict_scale(file_input,real_scale)


show_perf_test_one_scale("Cd",10,"CleanGuitar")

predict_scale_show(file_input,real_scale)

scale=get_max_notes(file_input)


target_folder = 'outputs/' + os.path.splitext(file_input)[0]

new_scale = Scale(scale, target_folder)

list_intervals = new_scale.get_list_intervals()

list_positions = new_scale.get_list_positions_in_scale()

list_corresponding_scales = new_scale.get_list_corresponding_scales()

list_english_notation = new_scale.get_list_english_notation()

new_scale.generate_fretboard_svg()

new_scale.save_result_to_csv()

"""