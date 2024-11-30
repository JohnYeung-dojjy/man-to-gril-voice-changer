import numpy as np
import librosa
import matplotlib.pyplot as plt


class AudioProcessor:
    def __init__(self,
        sr: int = 44100,
    ):
        dt = 1/sr
        t = np.arange(0, 1, dt)
        self.window_length = len(t)
        self.frequency = (1 / (dt * self.window_length)) * np.arange(self.window_length)
        self.L = np.arange(1, np.floor(self.window_length / 2), dtype=np.int64)

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
        # [0.25, 0.5, 0.25], [0.05, 0.2, 0.5, 0.2, 0.05]
        gaussian = np.array([0.05, 0.2, 0.5, 0.2, 0.05])
        average = np.array([1, 1, 1, 1, 1, 1, 1])/7
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