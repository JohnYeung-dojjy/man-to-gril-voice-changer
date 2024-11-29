from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sys

class App:
    def __init__(self, system_arguments: list[str]):
        self.app = QApplication(system_arguments)
        self.app_main_window = QMainWindow()
        self.ui_main_window = uic.loadUi(Path("ui", "control.ui"), self.app_main_window)


    def show_window(self):
        self.app_main_window.show()

    def run(self):
        """Start the pyqt event loop, return the exit code"""
        return self.app.exec_()

def main(system_arguments: list[str]):
    app = App(system_arguments)
    app.show_window()

    app_return_status = app.run()
    sys.exit(app_return_status)

if __name__ == "__main__":
    system_arguments = sys.argv
    main(system_arguments)