import time

import queue
import numpy as np
import sounddevice as sd
import scipy
from scipy import fftpack


sol = 299792458 / 100000  # This is the speed of light in nm/s


class NoteRecognizer:
    
    def __init__(self, device=1, samplerate=44100, channels=2, downsample=10, window=1000):
        self.channels = channels
        self.downsample = downsample
        self.device = device
        self.samplerate = samplerate
        self.window = window
        self.mapping = [c - 1 for c in range(self.channels)]
        self.q = queue.Queue()
        
        self.length = int(self.window * self.samplerate / (1000 * self.downsample))
        self.data = np.zeros((self.length, self.channels))
        
        self.stream = sd.InputStream(device=self.device,
                                    channels=self.channels,
                                    samplerate=self.samplerate,
                                    callback=self._audio_callback)
        self.stream.start()
        self.hz = 0

    def _audio_callback(self, indata, frames, time, status):
        """
        This is called (from a separate thread) for each audio block.
        """
        if status:
            print('Error:', status)

        self.q.put(indata[::self.downsample, self.mapping])

    def update(self):
        """
        :returns str: recognized note
        """
        while True:
            try:
                data = self.q.get_nowait()
            except queue.Empty:
                break
                
            shift = len(data)
            self.data = np.roll(self.data, -shift, axis=0)
            self.data[-shift:, :] = data

        # Calculate wavelength
        lengths = []
        last_peak = 0

        for i, d in enumerate(self.data):
            if np.max(d) > 0.07:
                if last_peak != 0:
                    last_peak = i
                else:
                    lengths.append(i - last_peak)
                    last_peak = 0

        if lengths != []:
            wavelength = sum(lengths) / len(lengths)
            if wavelength != 0:
                self.hz = int(sol / wavelength)

        return self.hz
