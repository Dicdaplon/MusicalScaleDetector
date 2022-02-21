

#Internal libraries



from Function import *





class Audio :
    real_scale=0
    spectrum=0
    frequencies=0
    max_notes=0
    scale=0
    peaks_value=0
    peaks_hz=0
    peaks_notes=0

    def __init__(self, filename, scale):
        self.real_scale=scale
        self.rate, self.sample = scipy.io.wavfile.read(filename, mmap=False)

    def fft(self):
        self.spectrum,self.frequencies =get_fft(self.sample, self.rate)

    def smooth_fft(self, smoothing_value):
        self.spectrum = scipy.ndimage.gaussian_filter1d(self.spectrum, smoothing_value, order=0)

    def find_peaks(self):
        peaks, _ = find_peaks(self.spectrum, height=max(self.spectrum) / 4)
        self.peaks_value=self.frequencies[peaks]
        self.peaks_hz = self.frequencies[peaks]
        self.peaks_notes = hz_to_note_array(self.peaks_hz)

    def fft_show(self):
        Show_fft(self.spectrum, self.frequencies, self.real_scale)



