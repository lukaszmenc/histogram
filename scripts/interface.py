from PyQt5 import QtWidgets, QtCore

from scripts.file_operations import get_file_path, get_data_from_csv


class Interface(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.appname = "Histogram"
        self.resize(1280, 640)

        self.dataframe = None
        self.filepath = None

        self.columns = QtWidgets.QListWidget()

        self.main_window()

    def open_file(self):
        self.filepath = get_file_path()
        if self.filepath:
            df = get_data_from_csv(self.filepath)
            self.columns.clear()
            for col_name in [x for x in df.columns]:
                self.columns.addItem(col_name)
            self.columns.update()
            self.dataframe = df
        print(self.dataframe)

    def main_window(self):
        button_open_file = QtWidgets.QPushButton("Open CSV file")
        button_open_file.clicked.connect(lambda: self.open_file())
        button_create_histogram = QtWidgets.QPushButton("Create histogram")
        button_save = QtWidgets.QPushButton("Save histogram")
        button_save_report = QtWidgets.QPushButton("Save DOC report")

        save_layout = QtWidgets.QHBoxLayout()
        save_layout.addWidget(button_save)
        save_layout.addWidget(button_save_report)

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

        menu = QtWidgets.QVBoxLayout()
        menu.addWidget(button_open_file)
        menu.addLayout(parameters)
        menu.addWidget(self.columns)
        menu.addWidget(button_create_histogram)
        menu.addLayout(save_layout)

        menu_widget = QtWidgets.QWidget()
        menu_widget.setLayout(menu)
        menu_widget.setFixedWidth(320)

        window = QtWidgets.QHBoxLayout()
        window.setAlignment(QtCore.Qt.AlignLeft)
        window.addWidget(menu_widget)

        self.setLayout(window)
        self.setWindowTitle(self.appname)
        self.show()
