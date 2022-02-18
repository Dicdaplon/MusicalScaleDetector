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


def get_positions_in_scale_list(list_intervals):
    """
    Compute a list of positions inside a scale from an intervals list
    Parameters:
    list_intervals: list of integers

    Return
    list_positions: list of integers
    """

    list_positions = [0]

    for i in range(0, len(list_intervals)):
        list_positions.append(list_positions[i] + list_intervals[i])

    print('Position in scale :', list_positions)

    return list_positions


def get_intervals_list(detected_notes_list, note_key=None):
    """
    Compute the intervals from the raw data retrieve from get_max_notes. By default, the key of the scale is the first
    value in the input np.array
    Parameters:
    detected_notes_list: np.array
    note_key: integer, the user can specify a key

    Return
    list_intervals: list if integers
    """

    print('Raw input from get_max_notes: ', detected_notes_list)

    if (note_key is None):

        # considering the first note as the key of the
        key_note = detected_notes_list[0]

    print('The key note is the following: ', key_note)

    # sorting the array in ascending order
    detected_notes_list = np.sort(detected_notes_list)

    print('Sorted scale: ', detected_notes_list)

    # rearranging the array to get the key as the first element
    key_note_index = np.where(detected_notes_list == key_note)
    scale = np.roll(detected_notes_list, len(detected_notes_list) - key_note_index[0])

    print('Rearranged scale: ', scale)

    # computing the scale's intervals as a list
    list_intervals = []

    for note_index in range(0, len(scale) - 1):
        list_intervals.append(get_interval(detected_notes_list[note_index], detected_notes_list[note_index + 1]))

    print('Intervals list: ', list_intervals)

    return list_intervals

def get_corresponding_scales(input_notes_list):
    """
    Search for the corresponding scales in a csv file
    Parameters:
    input_notes_list: list of integer (values between 0 and 11)

    Return:
    selected_scales: list of corresponding scales
    """


    print(input_notes_list)

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

    # Searching for scale with beginning with the same string list
    selected_scales = df_scales.loc[df_scales['combined'].str.startswith(input_notes_list)]

    return selected_scales['scale'].to_list()