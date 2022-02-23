
from Audio import *
from fretboardgtr import ScaleGtr
from Scale import *
import os
import pandas as pd
# Choose your sample here


real_scale = "C"
type_of_sample = "Sinus"
output_folder = 'outputs/'

real_scale = "D"
type_of_sample = "CleanGuitar"
output_folder = 'outputs/' + type_of_sample + '/' + real_scale + '/'


# Number of files for given sample and scale
path_directory = './Sample/' + type_of_sample + '/' + real_scale
list_files = os.listdir(path_directory) # dir is your directory path
number_files = len(list_files)

real_scale = "D"
type_of_sample = "CleanGuitar"

file_input=get_sample_filepath(real_scale,6,type_of_sample)
print("file_input", file_input)

Audio_Obj = Audio(file_input, real_scale)
Audio_Obj.stft(0.2,5)
Audio_Obj.smooth_fft(1)
Audio_Obj.find_peaks_and_unique()
Audio_Obj.sort_peaks()
print(Audio_Obj.peaks_notes)
print(Audio_Obj.peaks_value)
print(Audio_Obj.unique_max_notes)
print(Audio_Obj.unique_max_notes_power)
Audio_Obj.fft_show(True)

