import queue

import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


device = 1
samplerate = 44100
channels = [0, 1]
window = 1000
interval = 30
downsample = 10
mapping = [c - 1 for c in channels]  # Channel numbers start with 1
q = queue.Queue()

length = int(window * samplerate / (1000 * downsample))
plotdata = np.zeros((length, len(channels)))
fig, ax = plt.subplots()
lines = ax.plot(plotdata)

# Draw channel labels
if len(channels) > 1:
    ax.legend(['Channel {}'.format(c) for c in channels], loc='lower left', ncol=len(channels))

ax.axis((0, len(plotdata), -1, 1))
# ax.set_yticks([0])
ax.yaxis.grid(True)
# ax.tick_params(bottom=False, top=False, labelbottom=False, right=False, left=True, labelleft=False)
fig.tight_layout(pad=0)


def audio_callback(indata, frames, time, status):
    """
    This is called (from a separate thread) for each audio block.
    """
    if status:
        print('Error:', status)

    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata[::downsample, mapping])


def update_plot(frame):
    """
    This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.
    """
    global plotdata, lines

    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data

    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])

    return lines


STREAM = sd.InputStream(device=device, channels=max(channels), samplerate=samplerate, callback=audio_callback)
ANIMATION = FuncAnimation(fig, update_plot, interval=interval, blit=True)

with STREAM:
    plt.show()
