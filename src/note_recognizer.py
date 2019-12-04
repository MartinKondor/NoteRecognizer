import queue
import numpy as np
import sounddevice as sd


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
            
        return np.max(self.data[:, 0]) + np.max(self.data[:, 1])
