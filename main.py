from Audio import *
from fretboardgtr import ScaleGtr
from Scale import *
import os
import pandas as pd
from scipy import signal
# Choose your sample here


real_scale="C"
type="Sinus"
sample_number=5

file_input= get_sample_filepath(real_scale,sample_number,type)

refscale= LettersToNumbers(getscalelist("D"))
output="C:/Users/chafik/Desktop/PyCharmProject/MusicalScaleDetector/MusicalScaleDetector/outputs"
Scale_Obj = Scale(refscale,file_input,output,2)
Scale_Obj.get_list_intervals()
Scale_Obj.get_list_positions_in_scale()

Audio_obj= Audio(file_input,real_scale)
sos= signal.butter(4, 400, 'hp', fs=44100, output='sos')
Audio_obj.sample = signal.sosfilt(sos, Audio_obj.sample)
Audio_obj.fft(15)

#Audio_obj.fft_show(True)
stft_live(file_input,type,real_scale,0.4,0.2,10)