from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from media_manager import MediaManager

from dataclasses import dataclass

@dataclass
class VoiceChangerStatus:
    mic_on: bool = False
    voice_changing: bool = False
    denoising: bool = False

class AppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.media_manager = MediaManager()
        self.vc_status = VoiceChangerStatus()

        uic.loadUi(Path("ui", "control.ui"), self)

        print(sorted(list(self.__dict__.keys())))

    @QtCore.pyqtSlot()
    def on_mic_btn_clicked(self):
        # toggle the btn
        self.vc_status.mic_on = not self.vc_status.mic_on
        icon = self.media_manager.mic_on_icon if self.vc_status.mic_on else self.media_manager.mic_off_icon
        self.mic_btn.setIcon(icon)

    @QtCore.pyqtSlot()
    def on_voice_change_btn_clicked(self):
        # toggle the btn
        self.vc_status.voice_changing = not self.vc_status.voice_changing
        icon = self.media_manager.changer_on_icon if self.vc_status.voice_changing else self.media_manager.changer_off_icon
        self.voice_change_btn.setIcon(icon)

    @QtCore.pyqtSlot()
    def on_denoise_btn_clicked(self):
        # toggle the btn
        self.vc_status.denoising = not self.vc_status.denoising
        self.denoise_btn.setText(f"Denoise? {'Y' if self.vc_status.denoising else 'N'}")

    @QtCore.pyqtSlot(int) # somehow does not work if type is not given
    def on_n_steps_slider_valueChanged(self, value):
        self.n_steps_value.setText(f"{value / 10}")

    @QtCore.pyqtSlot(int) # somehow does not work if type is not given
    def on_octave_slider_valueChanged(self, value):
        self.octave_value.setText(f"{value / 10}")
