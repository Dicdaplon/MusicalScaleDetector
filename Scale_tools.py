import numpy as np

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
    """
    Function to get list of pitch (str) contained in Chromatic scale starting from C
    Parameters: None
    Return : (str array) list of pitch from
    """
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
    """
    Return the corresponding n Indexe on freqaxes from a frequency (Hz)
    Parameters :
    hz : (float) Choosen frequency (Hz)
    freqaxe: (float array) Frequncies axes (Hz)
    return :
    n= (int) equivalent n index
    """
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