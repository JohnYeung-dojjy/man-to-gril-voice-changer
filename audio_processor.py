from typing import Any, Callable
import numpy as np
import librosa
import resampy # This was lazily loaded in librosa, load it first before overhead when calling librosa function
import matplotlib.pyplot as plt
from PyQt5 import QtCore
import sounddevice as sd

class AudioProcessor:
    def __init__(self,
        sr: int = 44100,
    ):
        self.stream = sd.Stream(
            samplerate=sr,
            blocksize=sr,
            channels=1, # single channel only
        )
        self.sr = sr
        dt = 1/sr
        t = np.arange(0, 1, dt)
        self.window_length = len(t)
        self.frequency = (1 / (dt * self.window_length)) * np.arange(self.window_length)
        self.L = np.arange(1, np.floor(self.window_length / 2), dtype=np.int64)

    def read_from_input_stream(self):
        """Read frames from the stream and return them, output shape is (frames, channels), in our case channel is 1"""
        frames, status = self.stream.read(self.sr)
        return frames

    def write_to_output_stream(self, data: np.ndarray):
        """Write data to the output stream, shape should be (frames, channels), in our case channel is 1"""
        underflowed = self.stream.write(data)

    def start_stream(self):
        """This method starts both input and output audio stream"""
        self.stream.start()

    def close_stream(self):
        """close the stream, called after the application event loop ended"""
        self.stream.stop()
        self.stream.close()

    # special thanks to https://youtu.be/s2K1JfNR7Sc
    # a hands to hands fft denoise tutorial/lecture
    def de_noise(self, data: np.ndarray):
        fhat = np.fft.fft(data.squeeze(), self.window_length)
        power = fhat * np.conj(fhat)

        indices = power > 1
        fhat = indices * fhat

        plt.plot(self.frequency[self.L], power.real[self.L])
        plt.xlim(self.frequency[self.L[0]], 500)
        plt.show()

        return np.fft.ifft(fhat).real

    def smooth(self, data: np.ndarray):
        """Smooth the audio data by applying a convolve filter"""
        # [0.25, 0.5, 0.25], [0.05, 0.2, 0.5, 0.2, 0.05]
        # need to be float32 to match sounddevice stream
        gaussian = np.array([0.05, 0.2, 0.5, 0.2, 0.05], dtype=np.float32)
        average = np.array([1, 1, 1, 1, 1, 1, 1], dtype=np.float32) / 7
        return np.convolve(data, average, "same")

    #Extract Freq in similar to remove noise
    def extract_freq(self, data: np.ndarray, n_steps: int):
        fhat = np.fft.fft(data.squeeze(), self.window_length)
        psd = fhat * np.conj(fhat) / self.window_length

        indices = psd > 1
        fhat = indices * fhat
        psdClean = indices * psd

        fhat2 = np.zeros(self.window_length,dtype=np.complex128)
        divi = n_steps
        half = self.window_length//n_steps
        for i in range(half):
            fhat2[divi * i] = (fhat[(divi-1)*i] + 0)/2
            fhat2[divi * (i + 1) - 1] = (fhat[(divi - 1) * (i+1) - 1] + 0) / 2
            for j in range(divi - 1):
                fhat2[divi * i + j + 1] = (fhat[(divi-1)*i+j] + fhat[(divi-1)*i+j+1])/2
        fhat2 = 0.88 * fhat2

        psd2 = fhat2 * np.conj(fhat2) / self.window_length
        indices2 = psd2 > 1
        psdClean2 = indices2 * psd2

        plt.plot(self.frequency[self.L], psdClean.real[self.L])
        plt.plot(self.frequency[self.L], psdClean2.real[self.L])
        plt.xlim(self.frequency[self.L[0]], 500)

        plt.show()

        return np.fft.ifft(fhat2).real

    def change_voice(self, data: np.ndarray, n_steps: float, bins_per_octave: int):
        """apply voice change algorithm

        Args:
            data (np.ndarray): transformed audio stream data of shape (frames,)
            n_steps (float): multiplier to the pitch level
            bins_per_octave (int): adder to the pitch level

        Returns:
            frequency changed audio stream data of shape (frames,): _description_
        """
        base_freq_shift = librosa.effects.pitch_shift(
            data, sr=self.sr, n_steps=n_steps, bins_per_octave=bins_per_octave, res_type="kaiser_fast"
        )
        harmonic_freq_shift = librosa.effects.pitch_shift(
            data, sr=self.sr, n_steps=n_steps*1.5, bins_per_octave=bins_per_octave, res_type="kaiser_fast"
        )
        data = 0.25 * base_freq_shift + 0.75 * harmonic_freq_shift
        data = self.smooth(data)
        return data
