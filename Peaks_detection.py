from Scale_tools import *
from scipy.signal import find_peaks

def sort_peaks(peaks_value,peaks_hz):
    """
    Sort detected peaks by value,sort a reorder peaks_value and peaks_note too
    Parameter:
    peaks_value: (float array) detected peaks power
    peaks_hz: (float array) detected peaks localisation in hz
    return:
    (float array) sorted peaks_value, (float array) sorted peaks_hz, (str array) sorted peaks_char
    """
    max_value_index=np.argsort(peaks_value)
    max_value_index=max_value_index[::-1]
    peaks_value=np.sort(peaks_value)
    new_peaks_value=peaks_value[::-1]

    new_peaks_hz=np.zeros(len(peaks_hz))
    for n in range(0,len(max_value_index)) :
        new_peaks_hz[n]=peaks_hz[max_value_index[n]]

    new_peaks_char=hz_to_note_array(new_peaks_hz)

    return new_peaks_value, new_peaks_hz, new_peaks_char


def unique_peaks(peaks_value,peaks_note):
    """
    get array of unique notes from peaks, classing them by cumulating power for every same note
    Parameter:
    peaks_value: (float array) detected peaks power
    peaks_note: (str array) detected peaks notes equivalent
    return:
    (float array) new_peak_value,(str array) new_peaks_char
        """
    listscale=listscale_from_dict()
    new_peaks_value=np.zeros(len(listscale))
    new_peaks_note = []
    for n in range(0,len(listscale)) :
        new_peaks_note.append(listscale[n])
        sum = 0
        for m in range(0,len(peaks_value)):
            if listscale[n]== peaks_note[m]:
                sum = sum+peaks_value[m]
        new_peaks_value[n]=sum

    new_peaks_note2= []
    index_max=np.argsort(new_peaks_value)
    index_max=index_max[::-1]
    for n in range(0,len(new_peaks_note)):
        new_peaks_note2.append(new_peaks_note[index_max[n]])

    new_peaks_value=np.sort(new_peaks_value)
    new_peaks_value=new_peaks_value[::-1]

    return new_peaks_value, new_peaks_note2