from Audio import *

real_scale="C"
type="CleanGuitar"
sample_number=4




file_input= get_sample_filepath(real_scale,sample_number,type)

Audio_obj= Audio(file_input,real_scale)
Audio_obj.spectrum_process()
Audio_obj.pitch_recognition()
print("sorted pitch are",Audio_obj.unique_max_notes)

output="\outputs"
Scale_obj= Scale([0,2,4,5,7,9,11],file_input,output,'C')
Scale_obj.get_list_intervals()
Scale_obj.get_list_positions_in_scale()
Scale_obj.get_list_corresponding_scales()
Scale_obj.get_list_english_notation()
Scale_obj.generate_fretboard_svg()