import sklearn
import scipy
import scipy
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from scipy.io import wavfile
import scipy.io


from Function import *
from FFTfunction import *
from TEST import *


rate,audio_data=scipy.io.wavfile.read("C.wav", mmap=False)
#Pow,Axes= get_fft(audio_data,rate)
#Pow,Axes=get_stft(audio_data,0.1,9,rate)
audio_data=audio_data[int(9*(len(audio_data)/20)):int((10*len(audio_data)/20))]
Pow,Axes=get_summed_stft(audio_data,0.025,rate)
Pow,Axes=normalizeFFT(Pow,Axes)
Pow,Axes=FFTtrunc(Pow,Axes,80,3200)
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
fig.savefig('test2png.png', dpi=100)
plt.xscale("log")
plt.plot(Axes,Pow)
plt.show()
