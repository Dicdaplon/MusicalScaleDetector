from Audio import *
from Scale import *
import os
# Choose your sample here

real_scale = "C"
type_of_sample = "CleanGuitar"
output_folder = 'outputs/'

# Number of files for given sample and scale
path_directory = './Sample/' + type_of_sample + '/' + real_scale
list_files = os.listdir(path_directory) # dir is your directory path
number_files = len(list_files)

for number in range(0, number_files):

    sample_number = number

    # Don't touch zone
    file_input = get_sample_filepath(real_scale, sample_number, type_of_sample)

    print('file_input', file_input)

    # Have fun zone (supress and test all you want)
    Audio_Obj = Audio(file_input, output_folder, real_scale)
    print(Audio_Obj.sample)
    Audio_Obj.fft()
    Audio_Obj.smooth_fft(30)
    Audio_Obj.find_peaks()
    Audio_Obj.find_max_notes_peaks()
    Audio_Obj.fft_show()
    scale=Audio_Obj.max_notes_char

    # predict_scale(file_input,real_scale)

    # show_perf_test_one_scale("C", 10, "CleanGuitar", output_folder)

    # predict_scale_show(file_input, real_scale, output_folder)

    scale = Audio_Obj.max_notes_number

    print("output scale ", scale)

    # To
    scale = np.unique(scale)
    scale = scale.astype(int)

    new_scale = Scale(scale, file_input, output_folder)

    list_intervals = new_scale.get_list_intervals()

    list_positions = new_scale.get_list_positions_in_scale()

    list_corresponding_scales = new_scale.get_list_corresponding_scales()

    list_english_notation = new_scale.get_list_english_notation()

    new_scale.generate_fretboard_svg()

    new_scale.save_result_to_csv()
