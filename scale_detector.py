import numpy as np
import pandas as pd


def get_interval(first_note, second_note):
    """
    Computes the interval between to note according to the index
    Parameters:
    first_note: integer (between 0 and 11)
    second_note: integer (between 0 and 11)

    Return:
    interval: integer
    """

    if (first_note < second_note):

        interval = second_note - first_note

    else:

        interval = (11 - first_note) + second_note + 1

    return interval


def get_corresponding_scale(input_notes_list):

    # Loading csv file
    df_scales = pd.read_csv('music-scales.csv', header=None, names=['scale', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])

    # Computing columns value to integer
    df_scales.loc[:, df_scales.columns != 'scale'] = df_scales.loc[:, df_scales.columns != 'scale'].fillna(0).astype('int32')

    # Computing columns value into a combined list
    df_scales['combined'] = df_scales.loc[:, df_scales.columns != 'scale'].values.tolist()

    # Computing combined column into string
    df_scales['combined'] = df_scales['combined'].astype('str')

    # Transforming input notes as a string
    input_notes_list = str(input_notes_list)
    input_notes_list = input_notes_list[:-1]

    selected_scales = df_scales.loc[df_scales['combined'].str.startswith(input_notes_list)]

    return selected_scales['scale'].to_list()

# getting the actual result from get_max_note function
scale = [9, 11,  7,  8,  4,  6, 10]
#scale = np.array([7, 9, 8, 0, 4, 2, 5])

print('Raw input from get_max_notes: ', scale)

# considering the first note as the key of the
key_note = scale[0]

print('The key note is the following: ', key_note)

# sorting the array in ascending order
scale = np.sort(scale)

print('Sorted scale: ', scale)

# rearranging the array to get the key note as the first element
key_note_index = np.where(scale == key_note)
scale = np.roll(scale, len(scale) - key_note_index[0])

print('Rearranged scale: ', scale)

# computing the scale's intervals as a list
list_intervals = []

for note_index in range(0,len(scale) - 1 ):

    list_intervals.append(get_interval(scale[note_index], scale[note_index+1]))

print('Intervals list: ', list_intervals)

list_positions = [0]

for i in range(0,len(list_intervals) - 1 ):

    list_positions.append(list_positions[i]  + list_intervals[i])

print('Position in scale :', list_positions)

corresponding_scales = get_corresponding_scale(list_positions)

print('List of corresponding scale : ', corresponding_scales)


