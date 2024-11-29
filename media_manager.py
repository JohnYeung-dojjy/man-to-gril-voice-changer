import os
from PyQt5 import QtGui

from settings import MEDIA_DIR

class MediaManager:
    def __init__(self):
        self.changer_on_icon = QtGui.QIcon(os.path.join(MEDIA_DIR, "changer_on.png"))
        self.changer_off_icon = QtGui.QIcon(os.path.join(MEDIA_DIR, "changer_off.png"))
        self.mic_on_icon = QtGui.QIcon(os.path.join(MEDIA_DIR, "mic_on.jpg"))
        self.mic_off_icon = QtGui.QIcon(os.path.join(MEDIA_DIR, "mic_off.jpg"))
