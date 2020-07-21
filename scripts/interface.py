from PyQt5 import QtWidgets, QtCore


class Interface(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.appname = "Histogram"
        self.resize(1280, 640)

        self.main_window()

    def main_window(self):
        button_open_file = QtWidgets.QPushButton("Open CSV file")

        label_lsl = QtWidgets.QLabel('LSL')
        value_lsl = QtWidgets.QLineEdit()
        label_usl = QtWidgets.QLabel('USL')
        value_usl = QtWidgets.QLineEdit()
        label_min = QtWidgets.QLabel('Min')
        value_min = QtWidgets.QLineEdit()
        label_max = QtWidgets.QLabel('Max')
        value_max = QtWidgets.QLineEdit()

        parameters = QtWidgets.QGridLayout()
        parameters.addWidget(label_lsl, 0, 0, 1, 1)
        parameters.addWidget(value_lsl, 0, 1, 1, 1)
        parameters.addWidget(label_usl, 0, 2, 1, 1)
        parameters.addWidget(value_usl, 0, 3, 1, 1)
        parameters.addWidget(label_min, 1, 0, 1, 1)
        parameters.addWidget(value_min, 1, 1, 1, 1)
        parameters.addWidget(label_max, 1, 2, 1, 1)
        parameters.addWidget(value_max, 1, 3, 1, 1)

        columns = QtWidgets.QListWidget()

        menu = QtWidgets.QVBoxLayout()
        menu.addWidget(button_open_file)
        menu.addLayout(parameters)
        menu.addWidget(columns)

        menu_widget = QtWidgets.QWidget()
        menu_widget.setLayout(menu)
        menu_widget.setFixedWidth(320)

        window = QtWidgets.QHBoxLayout()
        window.setAlignment(QtCore.Qt.AlignLeft)
        window.addWidget(menu_widget)

        self.setLayout(window)
        self.setWindowTitle(self.appname)
        self.show()
