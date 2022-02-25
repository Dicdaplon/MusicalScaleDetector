from Audio import *
from fretboardgtr import ScaleGtr
from Scale import *
import os
import pandas as pd
# Choose your sample here


real_scale="C"
type="CleanGuitar"
sample_number=5

file_input= get_sample_filepath(real_scale,sample_number,type)

refscale= LettersToNumbers(getscalelist("D"))
output="C:/Users/chafik/Desktop/PyCharmProject/MusicalScaleDetector/MusicalScaleDetector/outputs"
Scale_Obj = Scale(refscale,file_input,output,2)
Scale_Obj.get_list_intervals()
Scale_Obj.get_list_positions_in_scale()