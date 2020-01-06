import math

import queue
import numpy as np
import sounddevice as sd


class NoteRecognizer:

    def __init__(self, device=1, samplerate=44100, channels=2, downsample=10, window=1000):
        self.device = device
        self.samplerate = samplerate
        self.channels = channels
        self.downsample = downsample
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
        
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.A4 = 440
        self.C0 = self.A4 * math.pow(2, -4.75)
    
    def update(self):
        while True:
            try:
                data = self.q.get_nowait()
            except queue.Empty:
                break
                
            shift = len(data)
            self.data = np.roll(self.data, -shift, axis=0)
            self.data[-shift:, :] = data

        print(self.data)

        return 0

    def pitch_form_freq(self, freq):
        """
        Convert freqvency to note name.
        """
        h = round(12 * math.log2(freq / self.C0))
        octave = h // 12
        n = h % 12
        return self.note_names[n] + str(octave)

    def _audio_callback(self, indata, frames, time, status):
        """
        This is called (from a separate thread) for each audio block.
        """
        if status:
            print('Error:', status)

        self.q.put(indata[::self.downsample, self.mapping])

    def close(self):
        pass
