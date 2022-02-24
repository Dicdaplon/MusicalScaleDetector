#Internal libraries
import numpy as np

from FFTfunction import *
import os
from pathlib import Path


dict_notations_old = {
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


def listscale_from_dict():
    listscale=[]
    for n in range(0,12):
        listscale.append(dict_notations_old[n]["english_notation"])
    return listscale

def note_frequencies_construct(): #construct in Hz every note C to B including the # notes
    """
    Construct the frequencies (Hz) in the Chromatic scale from C
    Parameter: None
    return: (float) array of frequencies, size 12
    """
    gamme = np.zeros(12)
    gamme[0] = 65.4  # C (Do) at 32.7 Hz

    for i in range(1, len(gamme)): #construct every note in a chromatic scale
        gamme[i] = 1.05946 * gamme[i - 1]
    return gamme


def frequence_to_index(frequence, octave, freqaxe,rate):
    """
    Convert a frequency (Hz), doubled at the selected octave, to the n index corresponding
    Parameter:
    frequence: (float) Input frequency (Hz)
    octave: (int), 0 to get the selected frequency
    freqaxe: (float array), frequencies axe
    rate: (int), sample rate of audio file
    return: (int) frequency n index
    """
    freq_ind = frequence * np.power(2, octave)  # look for the selected freq and octave
    freq_ind = freq_ind + freqaxe[0]  # add a starting frequency as constant, fix for trunc function
    freq_ind = freq_ind * len(freqaxe) / rate  #transform frequence into indexes
    freq_ind=int(np.round(freq_ind))
    return freq_ind

def windows_hz_to_n(hz,freqaxe): #transform a windows in hz to a number of sample n
    hz=float(hz)
    df=freqaxe[1]-freqaxe[0]
    n=hz/df
    n=int(np.round(n))
    return n



def circularyscale(scale):  # transform scale a redondant value for the >11 (13 = 1, 12 = 0 )
    for n in range(0, len(scale)):
        if (scale[n] > 11):
            scale[n] = scale[n] - 12
    return scale



def getscalelist(note):
    listscale=listscale_from_dict()
    index=find_in_str_list(note,listscale)
    scale_numb=circularyscale(np.add([0, 2, 4, 5, 7, 9, 11],index))
    scale_char= NumberToLetter(scale_numb)
    return scale_char

def find_in_str_list(ourstr,list_str):
    index=-1
    for n in range(0,len(list_str)):
        if (ourstr == list_str[n]):
            index=n
    return index


def NumberToLetter(scale):
    listscale=listscale_from_dict()
    letterscale = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
    for n in range(0, len(scale)):
        letterscale[n] = listscale[scale[n]]
    letterscale=letterscale[0:len(scale)]
    return letterscale

def LetterToNumber(note_str):
    listscale = listscale_from_dict()
    number=find_in_str_list(note_str,listscale)
    return number


def LettersToNumbers(scaleChar):
    listscale=listscale_from_dict()

    number_scale=np.zeros(len(scaleChar))
    for n in range(0,len(scaleChar)):
        actual_str=scaleChar[n]
        #print(actual_str)
        number_scale[n]=int(LetterToNumber(actual_str))

    return number_scale


def Print_fft(Spectre,Freq,notescale,peaks, file_path=None): #need to implemant marker with the good note on the graph
    listscale = listscale_from_dict()
    scale=0
    for i in range (0,len(listscale)):
        if(listscale[i]==notescale):
            scale=i
    gamme = note_frequencies_construct()
    Biglistscale=listscale

    for n in range (0,scale):
        gamme=np.multiply(gamme,1.05946)#adapt scale frequency to selected scale
        listscale=np.concatenate([listscale,listscale])
    listscale=listscale[scale:12+scale]


    goodnote=[0,2,4,5,7,9,11]
    badnote=[1,3,6,8,10]

    Biglistscale=listscale
    Biggamme=gamme
    Biggoodnote=goodnote
    Bigbadnote=badnote

    for numberofscale in range(0,3):
        gamme=gamme*2
        Biggamme = np.concatenate([Biggamme, gamme])
        Biglistscale=np.concatenate([Biglistscale,listscale])
        goodnote=np.add(goodnote,12)
        Biggoodnote = np.concatenate([Biggoodnote,goodnote])
        badnote = np.add(badnote, 12)
        Bigbadnote = np.concatenate([Bigbadnote,badnote])

    plt.grid()
    maxfft=np.max(Spectre)
    plt.xlim(60,1000)
    for n in  Biggoodnote:
        plt.vlines(Biggamme[n], 0, maxfft, linestyles="dotted", colors="green")
        plt.text(Biggamme[n], 0, Biglistscale[n], color="green", fontsize=12)
    for n in  Bigbadnote:
        plt.vlines(Biggamme[n], 0, maxfft, linestyles="dotted", colors="red")
        plt.text(Biggamme[n], 0, Biglistscale[n], color="red", fontsize=12)


    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    #fig.savefig('test2png.png', dpi=100)
    plt.xscale("log")
    plt.plot(Freq, Spectre)
    if (len(peaks) != 1):
        plt.plot(Freq[peaks], Spectre[peaks], 'x')

    # if a file_path is given
    if file_path is not None:

        Path(file_path).mkdir(exist_ok=True, parents=True)
        plt.savefig(file_path + "/spectrogram.png", dpi=100)
        plt.clf()

def Show_fft(Spectre,Freq,notescale,peaks, blocking): #need to implemant marker with the good note on the graph
    listscale = listscale_from_dict()
    scale=0
    for i in range (0,len(listscale)):
        if(listscale[i]==notescale):
            scale=i
    gamme = note_frequencies_construct()
    Biglistscale=listscale

    for n in range (0,scale):
        gamme=np.multiply(gamme,1.05946)#adapt scale frequency to selected scale
        listscale=np.concatenate([listscale,listscale])
    listscale=listscale[scale:12+scale]


    goodnote=[0,2,4,5,7,9,11]
    badnote=[1,3,6,8,10]

    Biglistscale=listscale
    Biggamme=gamme
    Biggoodnote=goodnote
    Bigbadnote=badnote

    for numberofscale in range(0,3):
        gamme=gamme*2
        Biggamme = np.concatenate([Biggamme, gamme])
        Biglistscale=np.concatenate([Biglistscale,listscale])
        goodnote=np.add(goodnote,12)
        Biggoodnote = np.concatenate([Biggoodnote,goodnote])
        badnote = np.add(badnote, 12)
        Bigbadnote = np.concatenate([Bigbadnote,badnote])

    plt.grid()
    maxfft=np.max(Spectre)
    plt.xlim(60,2000)
    for n in  Biggoodnote:
        plt.vlines(Biggamme[n], 0, maxfft, linestyles="dotted", colors="green")
        plt.text(Biggamme[n], 0, Biglistscale[n], color="green", fontsize=12)
    for n in  Bigbadnote:
        plt.vlines(Biggamme[n], 0, maxfft, linestyles="dotted", colors="red")
        plt.text(Biggamme[n], 0, Biglistscale[n], color="red", fontsize=12)


    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    #fig.savefig('test2png.png', dpi=100)
    plt.xscale("log")
    plt.plot(Freq, Spectre)
    if (len(peaks) != 1):
        plt.plot(Freq[peaks], Spectre[peaks], 'x')

    plt.show(block =blocking)


def get_sample_filepath(real_scale,sample_number,type_of_sample):
    """
    Simple way to get filepath we can directly use
    Parameter:
    real_scale :  (str) as "C","Cd","D"...etc
    sample_number:  (int) number the test sample (don't exced 10)
    type_of_sample :  (str) type of bank, only "CleanGuitar" for now
    return: (str) filepath, you also have the groundtruth with real_scale
    """
    filepath = "Sample/" + type_of_sample + "/" + real_scale + "/" + real_scale + str(sample_number) + ".wav"
    return filepath


def show_perf_test_one_scale(scale, number_of_sample, type_of_sample, output_directory):
    """
        Test and show result of method for multiple samples of one scale
        Parameter:
        scale :  (str) as "C","Cd","D"...etc
        number_of_sample:  (int) number of samples you want to test (don't exced 10)
        type_of_sample :  (str) type of bank, only "CleanGuitar" for now
        return: None, only printing the result for now
        """

    print("Result for",number_of_sample,type_of_sample,"samples of ",scale, "scale")
    for n in range(0,number_of_sample):
        file_path=get_sample_filepath(scale,n,type_of_sample)
        print(predict_scale(file_path, scale, output_directory))

def hz_to_note (frequency):
    """
    Gave the nearest note corresponding to a frequency in Hz
    Parameter:
    frequency :  (float) Input freqency in Hz
    return: (str) nearest note
    """
    listscale = listscale_from_dict()
    limit_of_octave1=(123+131)/2
    while(frequency>limit_of_octave1):
        frequency=frequency/2
    note_ref=note_frequencies_construct()
    diff_with_ref=np.zeros(len(note_ref))

    for n in range(0,len(note_ref)):
        diff_with_ref[n]=np.abs(note_ref[n]-frequency)

    sorted_diff_index=np.argsort(diff_with_ref)
    note=listscale[sorted_diff_index[0]]

    return note

def hz_to_note_array (frequencies_array):
    """
        Gave the nearest notes correspondings for a frequencies array (Hz)
        Parameter:
        frequencies_array: (float array) Input frequency (Hz)
        return: (str array) notes array
        """
    notes_array = []
    for n in range(0, len(frequencies_array)):
        notes_array.append(hz_to_note(frequencies_array[n]))
    return notes_array


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

def scale_compare_score (charin,charref) :
    score =0
    for n in range (0,len(charin)):
        if(charin[n] in charref):
            score=score+(10/(n+1))
    fundamentals=[charref[0],charref[2],charref[4]]
    for n in range(0,len(fundamentals)):
        if(fundamentals[0] in charin):
            score = score+3
    return score

def scales_compares_scores (charin):
    scale_scores = np.zeros(11)
    for n in range(0, 11):
        refscale = np.add([0, 2, 4, 5, 7, 9, 11], n)
        fund = [refscale[0], refscale[2], refscale[4]]
        refscale= circularyscale(refscale)
        scale_scores[n] = scale_compare_score(charin, NumberToLetter(refscale))
    max_scores_index= np.argsort(scale_scores)
    max_scores_index=max_scores_index[::-1]
    listscale=listscale_from_dict()
    predicted_scale= listscale[max_scores_index[0]]
    return scale_scores, predicted_scale


def stft_live(file_input,type_of_sample,real_scale,windowstime,incremanttime):
    """
    Simulation of live chord solving
    Parameters :
    file_input:(str) path to the input file
    type_of_sample : (str) type of the sample
    real_scale: (str)  groundtruth_scale
    windonws_time : (float) time for every sample in the stft (s)
    incremanttime: speed of the windows along the sample (s, if < windows = overlapping)
    return :
    None
    """
    Audio_Obj = Audio(file_input, real_scale)
    max_n=   int((len(Audio_Obj.sample)/Audio_Obj.rate )-(2*windowstime))
    max_n= int(max_n/incremanttime)
    for incremant in range(0,max_n):
        Audio_Obj.stft(windowstime,windowstime+(incremant*incremanttime))
        seuil=(0.1)*np.max(Audio_Obj.spectrum)
        Audio_Obj.spectrum=Audio_Obj.spectrum*(Audio_Obj.spectrum> seuil)
        Audio_Obj.smooth_fft(10)
        Audio_Obj.sum_spectrum=Audio_Obj.sum_spectrum+Audio_Obj.spectrum
        Audio_Obj.find_peaks_and_unique_from_sum()
        print("Audio_Obj.unique_max_notes_power",Audio_Obj.unique_max_notes_power)
        plt.clf()
        #Audio_Obj.summed_stft_show(False)
        time =np.round(1+(incremant*incremanttime),decimals=2)
        plt.title("Time "+ str(time) +" s, "+ str(windowstime) +"s windows, increment every "+ str(incremanttime)+ "s ")
        max_plot_y=np.max(Audio_Obj.sum_spectrum)

        plt.text(230, 7*max_plot_y/8, "Pur " +type_of_sample+ real_scale+" Sample", fontsize=20)
        listx=[0,7,17,27,35,50,68,86,100,125,160,195]
        refscale = getscalelist(real_scale)
        for n in range(0, len(Audio_Obj.unique_max_notes)):
            x=60+ listx[n]
            if Audio_Obj.unique_max_notes[n] in refscale:
                plt.text(x, max_plot_y , Audio_Obj.unique_max_notes[n], fontsize=20,color="green")
            else:
                plt.text(x, max_plot_y, Audio_Obj.unique_max_notes[n], fontsize=20, color="red")

        listx = [0,70, 140, 190,270, 350, 440,540,650,760,870]
        refscale=getscalelist(real_scale)
        for n in range(0,len(refscale)):
            x=listx[n]
            plt.text(500+x, max_plot_y, refscale[n], fontsize=20, color="g")
        scalesscores, predicted_scale= scales_compares_scores(Audio_Obj.unique_max_notes[0:8])
        plt.text(230, 6*max_plot_y / 8, "Predicted Major Scale : "+ predicted_scale, fontsize=20)
        Audio_Obj.summed_stft_show(False)
        plt.pause(0.03)
    Audio_Obj.summed_stft_show(True)
class Audio :
    spectrum = 0
    sum_spectrum = 0
    frequencies = 0
    rate = 0
    real_scale=0
    unique_max_notes=0
    unique_max_notes_power=0
    scale=0
    peaks=np.ones(1)
    peaks_value=0
    peaks_hz=0
    peaks_notes=0
    max_notes_number=0
    max_notes_char = []
    time=0
    windows_time=0
    unique_max_notes_scale=0
    def __init__(self, filename, output_directory, scale):
        self.real_scale=scale
        self.rate, self.sample = scipy.io.wavfile.read(filename, mmap=False)

        # File result management
        self.output_directory = output_directory

        # Extraction of the file name in the given path without extension
        self.file_name = os.path.basename(filename)

        # Generation of result path
        self.result_path = "./" + self.output_directory + self.file_name

    def __init__(self, filename, scale):
        self.real_scale = scale
        self.rate, self.sample = scipy.io.wavfile.read(filename, mmap=False)

    def fft(self):
        self.spectrum,self.frequencies =get_fft(self.sample, self.rate)
        self.spectrum,self.frequencies =fft_trunc(self.spectrum,self.frequencies,0,8000)

    def stft(self,windows_time,where_time):
        self.spectrum, self.frequencies = get_stft(self.sample,windows_time,where_time, self.rate)
        self.spectrum, self.frequencies = fft_trunc(self.spectrum, self.frequencies, 0, 8000)
        self.time=where_time
        self.windows_time=windows_time

    def smooth_fft(self, smoothing_value):
        self.spectrum = scipy.ndimage.gaussian_filter1d(self.spectrum, smoothing_value, order=0)

    def find_peaks_and_unique(self):
        peaks, _ = find_peaks(self.spectrum, height=max(self.spectrum) / 4)
        self.peaks=peaks
        self.peaks_value=self.spectrum[peaks]
        self.peaks_hz = self.frequencies[peaks]
        self.peaks_notes = hz_to_note_array(self.peaks_hz)
        self.unique_max_notes_power,self.unique_max_notes=unique_peaks(self.peaks_value,self.peaks_notes)
        self.unique_max_notes_scale = LettersToNumbers(self.unique_max_notes)

    def find_peaks_and_unique_from_sum(self):
        peaks, _ = find_peaks(self.sum_spectrum, height=max(self.spectrum) / 4)
        self.peaks = peaks
        self.peaks_value = self.sum_spectrum[peaks]
        self.peaks_hz = self.frequencies[peaks]
        self.peaks_notes = hz_to_note_array(self.peaks_hz)
        self.unique_max_notes_power, self.unique_max_notes = unique_peaks(self.peaks_value, self.peaks_notes)
        self.unique_max_notes_scale = LettersToNumbers(self.unique_max_notes)

    def sort_peaks(self):

        self.peaks_value,self.peaks_hz, self.peaks_notes=  sort_peaks(self.peaks_value, self.peaks_hz)


    def find_max_notes_peaks(self):

        self.max_notes_char= hz_to_note_array(self.peaks_hz)
        self.max_notes_number=LettersToNumbers(self.max_notes_char)


    def fft_show(self, blocking):
        Show_fft(self.spectrum, self.frequencies, self.real_scale, self.peaks, blocking)

    def summed_stft_show(self, blocking):
        Show_fft(self.sum_spectrum, self.frequencies, self.real_scale, self.peaks, blocking)

    def fft_print(self):
        Show_fft(self.spectrum, self.frequencies, self.real_scale, self.peaks, self.result_path)



