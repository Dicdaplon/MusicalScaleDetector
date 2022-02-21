import numpy as np
import pandas as pd
import csv
from fretboardgtr import ScaleGtr
from pathlib import Path
from datetime import datetime
import os


def get_interval(first_note, second_note):
    """
    Computes the interval between to note according to the index
    Parameters:
    first_note: integer (between 0 and 11)
    second_note: integer (between pip 0 and 11)

    Return:
    interval: integer
    """

    if first_note < second_note:

        interval = second_note - first_note

    else:

        interval = (11 - first_note) + second_note + 1

    return interval


class Scale:
    """

    """

    def __init__(self, list_input_notes, input_file_path, output_directory, key_note=None):
        """
        Constructor of the Scale class, compute the list of note index in the right order and with the key note as
        the first note if none key_note is specified
        Parameters:
        list_input_notes: np.array of list from the notes detector function
        key_note: integer (0 to 11)
        """

        # Computing key_note and list of note index
        print('Raw input : ', list_input_notes)

        if key_note is not None:

            if key_note in list_input_notes:
                self.key_note = key_note
            else:
                print("The specified key note is not available, selecting the first note instead")
                self.key_note = list_input_notes[0]

        else:
            # Considering the first note as the key of the
            self.key_note = list_input_notes[0]

        print('The key note is the following: ', self.key_note)

        # sorting the array in ascending order
        list_input_notes = np.sort(list_input_notes)

        print('Sorted scale: ', list_input_notes)

        # rearranging the array to get the key as the first element
        key_note_index = np.where(list_input_notes == self.key_note)
        self.list_notes_index = np.roll(list_input_notes, len(list_input_notes) - key_note_index[0])

        print('Rearranged scale: ', self.list_notes_index)

        # Initialisation of a dictionary of notations
        self.dict_notations = {
            0: {"english_notation": 'C', "latin_notation": 'Do'},
            1: {"english_notation": 'C#', "latin_notation": 'Do#'},
            2: {"english_notation": 'D', "latin_notation": 'Re'},
            3: {"english_notation": 'D#', "latin_notation": 'Re#'},
            4: {"english_notation": 'E', "latin_notation": 'Mi'},
            5: {"english_notation": 'F', "latin_notation": 'Fa'},
            6: {"english_notation": 'F#', "latin_notation": 'Fa#'},
            7: {"english_notation": 'G', "latin_notation": 'Sol'},
            8: {"english_notation": 'G#', "latin_notation": 'Sol#'},
            9: {"english_notation": 'A', "latin_notation": 'La'},
            10: {"english_notation": 'A#', "latin_notation": 'La#'},
            11: {"english_notation": 'B', "latin_notation": 'Si'},
        }

        # Initialisation of different kind of lists of notations and data from the Scale
        self.list_notes_english_notation = []
        self.list_notes_latin_notation = []
        self.list_intervals = []
        self.list_positions_in_scale = []
        self.list_corresponding_scales = []

        self.output_directory = output_directory

        # Extraction of the file name in the given path without extension
        self.file_name = os.path.basename(input_file_path)

        # Generation of result path
        self.result_path = "./" + self.output_directory + self.file_name

    def get_list_intervals(self):
        """
        Compute the intervals from the raw data retrieve from get_max_notes. By default, the key of the scale is the first
        value in the input np.array
        Parameters:
        detected_notes_list: np.array
        note_key: integer, the user can specify a key

        Return
        list_intervals: list if integers
        """

        self.list_intervals = []

        for note_index in range(0, len(self.list_notes_index) - 1):
            self.list_intervals.append(
                get_interval(self.list_notes_index[note_index], self.list_notes_index[note_index + 1]))

        print('Intervals list: ', self.list_intervals)

        return self.list_intervals

    def get_list_positions_in_scale(self):
        """
        Compute a list of positions inside a scale from an intervals list
        Parameters:
        list_intervals: list of integers
        Return
        list_positions: list of integers
        """

        self.list_positions_in_scale = [0]

        if self.list_intervals is not []:

            for i in range(0, len(self.list_intervals)):
                self.list_positions_in_scale.append(self.list_positions_in_scale[i] + self.list_intervals[i])

            print('Positions in scale :', self.list_positions_in_scale)

            return self.list_positions_in_scale

        else:

            print("get_positions_in_scale_list needs a complete list of intervals from a Scale objet. Please call "
                  "get_list_invervals first")

    def get_list_corresponding_scales(self):
        """
        Search for the corresponding scales in a csv file
        Parameters:
        input_notes_list: list of integer (values between 0 and 11)

        Return:
        selected_scales: list of corresponding scales
        """

        self.list_corresponding_scales = []

        if self.list_positions_in_scale is not []:

            # Loading csv file
            df_scales = pd.read_csv('music-scales.csv', header=None,
                                    names=['scale', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])

            # Computing columns value to integer
            df_scales.loc[:, df_scales.columns != 'scale'] = df_scales.loc[:, df_scales.columns != 'scale'].fillna(
                0).astype('int32')

            # Computing columns value into a combined list
            df_scales['combined'] = df_scales.loc[:, df_scales.columns != 'scale'].values.tolist()

            # Computing combined column into string
            df_scales['combined'] = df_scales['combined'].astype('str')

            # Transforming input notes as a string
            input_notes_list = str(self.list_positions_in_scale)
            input_notes_list = input_notes_list[:-1]

            # Searching for scale with beginning with the same string list
            selected_scales = df_scales.loc[df_scales['combined'].str.startswith(input_notes_list)]

            self.list_corresponding_scales = selected_scales['scale'].to_list()

            print("List of corresponding scales : ", self.list_corresponding_scales)

            return self.list_corresponding_scales

        else:

            print("get_corresponding_scales needs the a list of positions. Please call get_list_positions_in_scale "
                  "first")

    def get_list_english_notation(self):
        """
        Generate a list with english notation from the list of index
        Parameter:
        list_notes_index
        """

        self.list_notes_english_notation = []

        for notes in self.list_notes_index:
            self.list_notes_english_notation.append(self.dict_notations[notes]['english_notation'])

        print('English notations list: ', self.list_notes_english_notation)

        return self.list_notes_english_notation

    def generate_fretboard_svg(self):
        """
        Save a fretboard.svg file according to the english notation. The file is saved in the output directory

        """

        root_english_notation = self.dict_notations[self.key_note]['english_notation']

        Path(self.result_path).mkdir( exist_ok=True)

        F = ScaleGtr(scale=self.list_notes_english_notation, root=root_english_notation)
        F.customtuning(['E', 'A', 'D', 'G', 'B', 'E'])
        F.theme(show_note_name=True)
        F.pathname(self.result_path + '/fretboard.svg')
        F.draw()
        F.save()


    def save_result_to_csv(self):
        """
        Save the main informations from the scale in a csv file in the specified directory folder
        """

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        dict_result = {
            "date": dt_string,
            "key_note": self.dict_notations[self.key_note]['english_notation'],
            "english_notation": self.list_notes_english_notation,
            "intervals": self.list_intervals,
            "position_in_scale": self.list_positions_in_scale,
            "list_of_corresponding_scales": self.list_corresponding_scales,
        }

        Path(self.result_path).mkdir(exist_ok=True)

        csv_file = self.result_path + '/result.csv'

        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.writer(csvfile)
                for key, value in dict_result.items():
                    writer.writerow([key, value])
        except IOError:
            print("I/O error")