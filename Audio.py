#Internal libraries

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

def get_max_notes(filename): #usefull for full test of the method  FOR BOUBOU
    """
    get_max_notes computes a wav file and extract the notes
    Parameter:
    filename: wav file

    return: list of detected notes
    """

    listscale=listscale_from_dict()
    print("every note is associated to a number as :")
    print(listscale)
    print([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    print("For Example the Cmajor scale :")
    print([0,2,4,5,7,9,11])

    oursong= Audio(filename)
    sample= oursong.sample
    rate = oursong.rate
    Spectre, Freq = get_fft(sample,rate)

    Spectre = scipy.ndimage.gaussian_filter1d(Spectre, 15, order=0)  #smoothing the FFT

    print('Size of Freq' ,str(len(Freq)))
    print('This is Freq', Freq)

    print('Size of spectre', str(len(Spectre)))
    print('This is spectre', Spectre)

    print("\n Power for every note : ")
    scores = score_for_everynote(Spectre, Freq, rate, 10) #return a vector of energy detected for every notes (float)
    for n in range(0, len(listscale)):
        print(listscale[n]," ", scores[n],"     ")


    scale = GetindexOfMaxNote(scores, 5)

    print("\n note detected ", scale)
    for n in range(0, len(scale)):
        print(listscale[scale[n]])


    return scale

def note_frequencies_construct(): #construct in Hz every note C to B including the # notes
    gamme = np.zeros(12)
    gamme[0] = 65.4  # C (Do) at 32.7 Hz

    for i in range(1, len(gamme)): #construct every note in a chromatic scale
        gamme[i] = 1.05946 * gamme[i - 1]
    return gamme


def frequence_to_index(frequence, octave, freqaxe,rate):
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


def note_score(spectre, freq, rate, note, windows):  # return summed score for a note C,Cd,D...
    listscale=listscale_from_dict()
    gamme = note_frequencies_construct()  # all the normalize value, C to B (Do vers Si) in Hz
    noteindex = listscale.index(note)  # reach for the indexes of the searched note (ex Cd -> 1)
    powerscale = 0
    n = noteindex
    np.max(spectre)
    spectre = spectre / np.max(spectre)
    for i in range(0, 6):
        freq_hz=gamme[n] * np.power(2, i)
        windows_hz=0.0544*freq_hz-0.0404  #regression adjustement, the windows increase with frequency
        windows=windows_hz_to_n(windows_hz, freq)
        windows= int(np.round(windows/2))
        freq_ind = frequence_to_index(gamme[n], i, freq,rate)  #need modification to doesn't take octave in parameter
        moyennage = np.mean(spectre[freq_ind - windows:freq_ind + windows + 1]) #maybe be not usefull...
        powerscale = powerscale + moyennage
    return powerscale



def score_for_everynote(spectre, freq,rate, windows):  # return vector of summed scores for each note C,Cd,D...
    powersvector = np.zeros(12);

    listscale=listscale_from_dict()
    n = 0
    for note in listscale:
        powersvector[n] = note_score(spectre, freq, rate, note, 30)
        n = n + 1
    return powersvector

def compare_with_known_scale (Scalein):
    listscale=listscale_from_dict()
    scoremax=0
    nmax=0
    for n in range(0,len(listscale)):
        refscale=np.add([0,2,4,5,7,9,11],[n,n,n,n,n,n,n])
        fundamentals=[refscale[0],refscale[2],refscale[4]]
        refscale,fundamentals=circularyscale(refscale,fundamentals)
        newscore=compare_vector(Scalein,refscale,fundamentals)
        if (newscore > scoremax):
            scoremax=newscore
            nmax=n

    return listscale[nmax]

def compare_vector(our, ref, fundamentals):  # compare 2 scale array and return a bool of identical value  BAD
    score = 0
    fundaments_found = [0, 0, 0]
    for n in range(0, len(our)):
        for m in range(0, len(ref)):
            ponderationRef = 1
            if (our[n] == ref[m]):
                if (ref[m] == fundamentals[0]):
                    fundaments_found[0]=1
                    ponderationRef = 10
                if (ref[m] == fundamentals[1]):
                    ponderationRef = 10
                    fundaments_found[1] = 1
                if (ref[m] == fundamentals[2]):
                    ponderationRef = 10
                    fundaments_found[2] = 1
                if (np.sum(fundaments_found) == 3):
                    ponderationRef = 100
                ponderationScaleIn = 10 / ((n+1)*(n+1))  #score added decrease with order (power) off note
                score = score + (10*ponderationScaleIn*ponderationRef)
    return score


def circularyscale(scale,fundamentals):  # transform scale a redondant value for the >11 (13 = 1, 12 = 0 )
    for n in range(0, len(scale)):
        if (scale[n] > 11):
            scale[n] = scale[n] - 12
    for n in range(0, len(fundamentals)):
        if (fundamentals[n] > 11):
            fundamentals[n] = fundamentals[n] - 12
    scale = np.sort(scale)  #bad idea to sort everything ?
    return scale,fundamentals


def FindScale(our):  # return a vector of better correspondance with known scale
    Scale = [0, 2, 4, 5, 7, 9, 11]
    our = circularyscale(our)
    sumscale = np.zeros(12)
    for scaleN in range(0, 11):
        newScale = circularyscale(Scale + scaleN * np.ones(len(Scale)))
        result = BoolReturn(newScale, our)
        sumscale[scaleN] = np.sum(result)

    return sumscale



def FindScaleFromvector(ScaleScoreVector):  # return a vector of better correspondance with known scale
    SortedScaleindex = np.argsort(ScaleScoreVector)
    SortedScaleindex = SortedScaleindex[::-1]
    listscale=listscale_from_dict()
    return listscale[SortedScaleindex[0]]


def GetindexOfMaxNote(ChordsPowersScores, Numberofvalues):

    Sortedindexs = np.argsort(ChordsPowersScores)  # return the indexes of sorted list (ascending)
    Sortedindexs = Sortedindexs[::-1]  # indexes of the list (decreasing)
    Sortedindexs = Sortedindexs[0:Numberofvalues]
    return Sortedindexs


def GetScale(filename):
    rate, audio_data = scipy.io.wavfile.read(filename, mmap=False)
    spectre, freq = get_fft(audio_data, rate)
    # spectre,freq = fft_trunc(spectre,freq,80,800)
    for i in range(0, 1):
        spectre, freq = GaussianFilterFFT(spectre, freq, [1, 1, 1, 1, 1])

    ChordsPowersScores =score_for_everynote(spectre, freq, 5)
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    Sortedindexs = GetindexOfMaxNote(ChordsPowersScores, 7)

    # Sortedindexs=np.sort(Sortedindexs)
    result = FindScale(Sortedindexs)
    result = FindScaleFromvector(result)

    return result

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
    return letterscale

def LetterToNumber(note_str):
    listscale = listscale_from_dict()
    number=find_in_str_list(note_str,listscale)
    return number


def LettersToNumbers(scaleChar):
    listscale=listscale_from_dict()
    print("Detected notes " , scaleChar)

    number_scale=np.zeros(len(scaleChar))
    for n in range(0,len(scaleChar)):
        actual_str=scaleChar[n]
        #print(actual_str)
        number_scale[n]=int(LetterToNumber(actual_str))

    return number_scale


def predict_scale_show(filename, realscale, output_directory): #usefull for full test of the method
    """
            Compute the method to the end with print and graph
            Parameter:
            filename :  (str) filepath of the sample
            realscale:  (str) groundtruth scale
            return: (str) predicted scale
            """
    oursong= Audio(filename,realscale, output_directory)

    oursong.fft()
    oursong.smooth_fft(45)



    scores = score_for_everynote(oursong.spectrum, oursong.frequencies,oursong.rate, 10)
    listscale=listscale_from_dict()

    for n in range(0, len(listscale)):
        print(listscale[n]," ", scores[n],"     ")


    scale = GetindexOfMaxNote(scores, 7)
    for n in range(0, len(scale)):
        print(listscale[scale[n]])


    for n in range(0, len(listscale)):
        refscale=np.add([0,2,4,5,7,9,11],[n, n, n, n, n, n, n])
        fundamentals = [refscale[0], refscale[2], refscale[4]]
        refscale,fundamentals=circularyscale(refscale,fundamentals)
        scalescore = compare_vector(scale, refscale,fundamentals)


    scaleChar = compare_with_known_scale(scale)
    print("\n\n  The good scale is", scaleChar)
    return scaleChar
    oursong.fft_show()

def predict_scale(filename, realscale, output_folder): #usefull for full test of the method
    """
        Compute the method to the end, no print, no show
        Parameter:
        filename :  (str) filepath of the sample
        realscale:  (str) groundtruth scale
        return: (str) predicted scale
        """
    oursong= Audio(filename,realscale, output_folder)
    sample= oursong.sample
    rate = oursong.rate
    Spectre, Freq = get_fft(sample,rate)

    Spectre = scipy.ndimage.gaussian_filter1d(Spectre, 15*3, order=0)

    scores = score_for_everynote(Spectre, Freq,rate, 10)
    listscale=listscale_from_dict()


    scale = GetindexOfMaxNote(scores, 7)


    scaleChar = compare_with_known_scale(scale)

    return scaleChar



def Show_fft(Spectre,Freq,notescale,peaks, file_path=None): #need to implemant marker with the good note on the graph
    listscale = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
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
    notes_array = []
    for n in range(0, len(frequencies_array)):
        notes_array.append(hz_to_note(frequencies_array[n]))
    return notes_array


class Audio :
    spectrum = 0
    frequencies = 0
    rate = 0
    real_scale=0
    max_notes=0
    scale=0
    peaks=np.ones(1)
    peaks_value=0
    peaks_hz=0
    peaks_notes=0
    max_notes_number=0
    max_notes_char = []

    def __init__(self, filename, output_directory, scale):
        self.real_scale=scale
        self.rate, self.sample = scipy.io.wavfile.read(filename, mmap=False)

        # File result management
        self.output_directory = output_directory

        # Extraction of the file name in the given path without extension
        self.file_name = os.path.basename(filename)

        # Generation of result path
        self.result_path = "./" + self.output_directory + self.file_name


    def fft(self):
        self.spectrum,self.frequencies =get_fft(self.sample, self.rate)

    def smooth_fft(self, smoothing_value):
        self.spectrum = scipy.ndimage.gaussian_filter1d(self.spectrum, smoothing_value, order=0)

    def find_peaks(self):
        peaks, _ = find_peaks(self.spectrum, height=max(self.spectrum) / 4)
        self.peaks=peaks
        self.peaks_value=self.spectrum[peaks]
        self.peaks_hz = self.frequencies[peaks]
        self.peaks_notes = hz_to_note_array(self.peaks_hz)

    def find_max_notes_peaks(self):

        self.max_notes_char= hz_to_note_array(self.peaks_hz)
        self.max_notes_number=LettersToNumbers(self.max_notes_char)


    def fft_show(self):
        Show_fft(self.spectrum, self.frequencies, self.real_scale, self.peaks, self.result_path)



