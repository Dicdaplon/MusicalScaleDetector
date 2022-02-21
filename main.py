from Audio import *

<<<<<<< HEAD

#Starting Zone
real_scale="C#"
=======
#choose your sample here

real_scale="C"
>>>>>>> 01c59949d897678849410cb80e83fd5f8c45ed62
sample_number=7
type_of_sample="CleanGuitar"


#Don't touch zone
file_input = get_sample_filepath(real_scale,sample_number,type_of_sample)



#Have fun zone (supress and test all you want)
Audio_Obj = Audio(file_input,real_scale)
print(Audio_Obj.sample)
Audio_Obj.fft()
Audio_Obj.smooth_fft(30)
Audio_Obj.find_peaks()
Audio_Obj.find_max_notes_peaks()


scale=Audio_Obj.max_notes_char


predict_scale(file_input,real_scale)


show_perf_test_one_scale("C",10,"CleanGuitar")

predict_scale_show(file_input,real_scale)

scale=Audio_Obj.max_notes_char


target_folder = 'outputs/' + os.path.splitext(file_input)[0]

new_scale = Scale(scale, target_folder)

list_intervals = new_scale.get_list_intervals()

list_positions = new_scale.get_list_positions_in_scale()

list_corresponding_scales = new_scale.get_list_corresponding_scales()

list_english_notation = new_scale.get_list_english_notation()

new_scale.generate_fretboard_svg()

new_scale.save_result_to_csv()
