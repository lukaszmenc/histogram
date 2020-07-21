from PyQt5 import QtWidgets, QtCore


class Interface(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.appnaame = "Histogram"
        self.resize(1280, 640)

        self.main_window()

    def main_window(self):
        window = QtWidgets.QHBoxLayout()
        window.setAlignment(QtCore.Qt.AlignLeft)

        self.setLayout(window)
        self.setWindowTitle(self.appname)
        self.show()
