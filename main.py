import numpy as np

from Audio import *
from scipy import signal
real_scale="C"
Type="CleanGuitar"
sample_number=3



file_input= get_sample_filepath(real_scale,sample_number,Type)

Audio_obj= Audio(file_input,real_scale)
sos = signal.butter(1, 800, 'hp', fs=44100, output='sos')
Audio_obj.sample = signal.sosfilt(sos, Audio_obj.sample)
Audio_obj.spectrum_process()
Audio_obj.process_peaks()
Audio_obj.process_pitches("max")



output="\outputs"
Scale_obj= Scale([0,2,4,5,7,9,11],file_input,output,'C')
Scale_obj.get_list_intervals()
Scale_obj.get_list_positions_in_scale()
Scale_obj.get_list_corresponding_scales()
Scale_obj.get_list_english_notation()
Scale_obj.generate_fretboard_svg()