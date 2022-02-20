import sklearn
import scipy
import scipy
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from scipy.io import wavfile
import scipy.io

class Audio :
    sample=0
    rate=0
    fft=0
    freq_axe=0
    max_notes=0
    scale=0

    def __init__(self, filename):
        self.rate, self.sample = scipy.io.wavfile.read(filename, mmap=False)




    #def get_fft(self,sample, rate):
     #   self.fft,self.freq_axe=get_fft(self,sample, rate)

