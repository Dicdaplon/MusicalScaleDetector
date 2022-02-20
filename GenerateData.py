from scipy.io import wavfile
import scipy.io


def little_sample_generator(filenamein,timeofeach,pathout,note):


    filenameout = pathout+"\\"+note
    print("filenamein", filenamein)
    rate,audio_data=scipy.io.wavfile.read(filenamein, mmap=False)
    number_of_sample= timeofeach*rate
    for n in range (0,int(len(audio_data)/number_of_sample)):
        part_data=audio_data[number_of_sample*n:number_of_sample*(n+1)]
        filenameout_number=filenameout+str(n)+".wav"
        scipy.io.wavfile.write(filenameout_number, rate, part_data)
        print("filenameout_number", filenameout_number)