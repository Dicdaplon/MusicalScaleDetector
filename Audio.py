#Internal library
from FFTfunction import *
from Scale import *
from Peaks_detection import *


#External Library
import scipy.io
from scipy.io import wavfile
import matplotlib.pyplot as plt



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
        print("peaks hz in show",Freq[peaks])

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







def stft_live(file_input,type_of_sample,real_scale,windowstime,incremanttime, smoothing):
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

    sos = signal.butter(1, 400, 'hp', fs=44100, output='sos')
    #Audio_Obj.sample = signal.sosfilt(sos, Audio_Obj.sample)

    max_n=   int((len(Audio_Obj.sample)/Audio_Obj.rate )-(2*windowstime))
    max_n= int(max_n/incremanttime)
    for incremant in range(0,max_n):
        Audio_Obj.stft(windowstime,windowstime+(incremant*incremanttime),smoothing)
        seuil=(0.1)*np.max(Audio_Obj.spectrum)
        Audio_Obj.spectrum=Audio_Obj.spectrum*(Audio_Obj.spectrum> seuil)
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
    #Temporal
    rate = 0
    time =0
    #FFT related
    spectrum = 0
    sum_spectrum = 0
    frequencies = 0
    windows_time = 0
    #Peaks related
    peaks = np.ones(1)
    peaks_value = 0
    peaks_hz = 0
    peaks_notes = 0
    #pitchs related
    unique_max_notes = 0
    unique_max_notes_power = 0
    unique_max_notes_scale = 0
    max_notes_number=0
    max_notes_char = []
    #Scale prediction related
    scale = 0
    real_scale = 0
    real_note_in_scale = []



    def __init__(self, filename, output_directory, scale):
        """
        Initialize with output file path
        Create an audio object with sample (array) and rate (int)
        """
        self.real_scale=scale
        self.rate, self.sample = scipy.io.wavfile.read(filename, mmap=False)

        # File result management
        self.output_directory = output_directory

        # Extraction of the file name in the given path without extension
        self.file_name = os.path.basename(filename)

        # Generation of result path
        self.result_path = "./" + self.output_directory + self.file_name

    def __init__(self, filename, scale):
        """
        Initialize an audi object without output path
        Create an audio object with sample (array) and rate (int)
        """
        self.real_scale = scale
        self.rate, self.sample = scipy.io.wavfile.read(filename, mmap=False)
        self.real_note_in_scale=getscalelist(scale)

    def spectrum_process(self):
        """"
        User friendly methods, compute the fft transform and the frequencies vector.
        Automated windows, padding, smoothing... for more control check fft and stft.
        Parameters : None
        return : None

        """
        self.process_fft(5)

    def pitch_recognition(self) :
        """
        User friendly methods, process the pitch in the musical sequence starting for the most present pitch
        Parameter : None
        return : None
        """
        self.find_peaks_and_unique()
    def process_fft(self,smoothing):
        """
        Compute and save the fft of the audio sample
        Parameters :
        smoothing :(int) value of gaussian 1D smoothing
        return :
        spectrum: (float array) Power Spectrum
        frequencies: (float array) array with corresponding frequencies of fft
        """
        self.spectrum,self.frequencies =get_fft(self.sample, self.rate)
        self.spectrum = scipy.ndimage.gaussian_filter1d(self.spectrum, smoothing, order=0)
        self.spectrum,self.frequencies =fft_trunc(self.spectrum,self.frequencies,0,8000)


    def stft(self,windows_time,where_time,smoothing):
        """
            Compute and save the short time windowed fft of the audio sample
            Parameters :
            windows_time : (float) size of the windows in s
            where_time : (float) temporal location of the windows in s
            smoothing :(int) value of gaussian 1D smoothing
            return :
            spectrum: (float array) Power Spectrum
            frequencies: (float array) array with corresponding frequencies of fft
                """
        self.spectrum, self.frequencies = get_stft(self.sample,windows_time,where_time, self.rate)
        self.spectrum = scipy.ndimage.gaussian_filter1d(self.spectrum, smoothing, order=0)
        self.spectrum, self.frequencies = fft_trunc(self.spectrum, self.frequencies, 0, 8000)
        self.time=where_time
        self.windows_time=windows_time


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

    def sort_peaks(self,sortby):
        """
        Sort peaks pitch, value and hz consistently, by the choosen axes
        Parameters:
        sortby : (str "hz" or "value") sort hz ascending order, or value descending order
        return: None
        """
        if sortby == "hz":
            reflist=self.peaks_hz
            self.peaks_hz, self.peaks_value = sort_2_list(reflist, self.peaks_value,"ascending")
            self.peaks_hz, self.peaks_notes = sort_2_list(reflist, self.peaks_notes,"ascending")
        if sortby== "value":
            reflist = self.peaks_value
            self.peaks_value, self.peaks_hz = sort_2_list(reflist, self.peaks_hz,"descending")
            self.peaks_value, self.peaks_notes = sort_2_list(reflist, self.peaks_notes,"descending")


    def find_max_notes_peaks(self):

        self.max_notes_char= hz_to_note_array(self.peaks_hz)
        self.max_notes_number=LettersToNumbers(self.max_notes_char)



    def fft_show(self, blocking):
        """"
        Show a graph with FFT and scale information
        Parameters:
        blocking : (Boolean) True for stopping the program when plotting
        return : None
        """
        Show_fft(self.spectrum, self.frequencies, self.real_scale, self.peaks, blocking)

    def summed_stft_show(self, blocking):
        Show_fft(self.sum_spectrum, self.frequencies, self.real_scale, self.peaks, blocking)

    def fft_print(self):
        Show_fft(self.spectrum, self.frequencies, self.real_scale, self.peaks, self.result_path)



