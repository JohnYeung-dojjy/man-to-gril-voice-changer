import os
from PyQt5 import QtGui

from settings import MEDIA_DIR

class MediaManager:
    def __init__(self):
        self.mic_on_icon = QtGui.QIcon(os.path.join(MEDIA_DIR, "micOn.png"))
        self.mic_off_icon = QtGui.QIcon(os.path.join(MEDIA_DIR, "micOff.png"))
        self.on_air_btn_icon = QtGui.QIcon(os.path.join(MEDIA_DIR, "on-air btn.jpg"))
        self.off_air_btn_icon = QtGui.QIcon(os.path.join(MEDIA_DIR, "off-air btn.jpg"))
