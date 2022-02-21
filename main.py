from Audio import *
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

for number in range(0, number_files):





real_scale = "C"
type_of_sample = "Sinus"

file_input=get_sample_filepath(real_scale,4,type_of_sample)
print("file_input", file_input)
Audio_Obj = Audio(file_input, real_scale)
Audio_Obj.fft()
Audio_Obj.smooth_fft(25)
Audio_Obj.find_peaks()
Audio_Obj.sort_peaks()
Audio_Obj.fft_show()

