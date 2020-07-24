from PyQt5 import QtWidgets, QtCore, QtGui
from PIL.ImageQt import ImageQt
from PIL import Image

from scripts.file_operations import get_file_path, get_data_from_csv
from scripts.data_operations import prepare_data, histogram


class Interface(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.appname = "Histogram"
        self.resize(1280, 640)

        self.dataframe = None
        self.filepath = None
        self.histogram = None

        self.value_lsl = QtWidgets.QLineEdit()
        self.value_lsl.textChanged.connect(lambda: self.change_histogram())
        self.value_usl = QtWidgets.QLineEdit()
        self.value_usl.textChanged.connect(lambda: self.change_histogram())
        self.value_min = QtWidgets.QLineEdit()
        self.value_min.textChanged.connect(lambda: self.change_histogram())
        self.value_max = QtWidgets.QLineEdit()
        self.value_max.textChanged.connect(lambda: self.change_histogram())

        self.columns = QtWidgets.QListWidget()
        self.image_label = QtWidgets.QLabel()
        self.image_label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.coeff_label = QtWidgets.QLabel()
        font = QtGui.QFont()
        self.coeff_label.setFont(QtGui.QFont(font.defaultFamily(), 12))
        self.coeff_label.setAlignment(QtCore.Qt.AlignHCenter)

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

    def create_histogram(self):
        try:
            column_name = [item.text() for item in self.columns.selectedItems()][0]
            data = prepare_data(self.dataframe, column_name)

            chart, coeffs = histogram(data, column_name, float(self.value_lsl.text()), float(self.value_usl.text()), self.value_min.text(), self.value_max.text())

            self.histogram = {'histogram': chart, 'data': coeffs}

            self.set_image()
            self.set_coeff()

        except IndexError:
            QtWidgets.QMessageBox.warning(
                None,
                "No data",
                'No column has been picked from the column list.\n'
                'Make sure a file has been loaded with "Open CSV file".',
                QtWidgets.QMessageBox.Ok,
            )
        except Exception as e:
            print(type(e).__name__, e)

    def change_histogram(self):
        if self.histogram:
            self.create_histogram()

    def set_image(self):
        image = Image.open(self.histogram['histogram'])
        pixmap = QtGui.QPixmap.fromImage(ImageQt(image))
        self.image_label.setPixmap(pixmap)

    def set_coeff(self):
        if self.histogram['data']:
            self.coeff_label.setText(
                f"\n\n\nCp: {self.histogram['data']['Cp']}\n"
                f"CPU: {self.histogram['data']['CPU']}\n"
                f"CPL: {self.histogram['data']['CPL']}\n"
                f"Cpk: {self.histogram['data']['Cpk']}\n"
                f"µ: {self.histogram['data']['mu']}\n"
                f"σ: {self.histogram['data']['sigma']}\n"
                f"min: {self.histogram['data']['min']}\n"
                f"max: {self.histogram['data']['max']}\n"
                f"ω: {self.histogram['data']['dominant']}"
            )
        else:
            self.coeff_label.setText('No data')

    def main_window(self):
        button_open_file = QtWidgets.QPushButton("Open CSV file")
        button_open_file.clicked.connect(lambda: self.open_file())

        button_create_histogram = QtWidgets.QPushButton("Create histogram")
        button_create_histogram.clicked.connect(lambda: self.create_histogram())

        button_save = QtWidgets.QPushButton("Save histogram")
        button_save_report = QtWidgets.QPushButton("Save DOC report")

        save_layout = QtWidgets.QHBoxLayout()
        save_layout.addWidget(button_save)
        save_layout.addWidget(button_save_report)

        label_lsl = QtWidgets.QLabel('LSL')
        label_usl = QtWidgets.QLabel('USL')
        label_min = QtWidgets.QLabel('Min')
        label_max = QtWidgets.QLabel('Max')

        parameters = QtWidgets.QGridLayout()
        parameters.addWidget(label_lsl, 0, 0, 1, 1)
        parameters.addWidget(self.value_lsl, 0, 1, 1, 1)
        parameters.addWidget(label_usl, 0, 2, 1, 1)
        parameters.addWidget(self.value_usl, 0, 3, 1, 1)
        parameters.addWidget(label_min, 1, 0, 1, 1)
        parameters.addWidget(self.value_min, 1, 1, 1, 1)
        parameters.addWidget(label_max, 1, 2, 1, 1)
        parameters.addWidget(self.value_max, 1, 3, 1, 1)

        menu = QtWidgets.QVBoxLayout()
        menu.addWidget(button_open_file)
        menu.addLayout(parameters)
        menu.addWidget(self.columns)
        menu.addWidget(button_create_histogram)
        menu.addLayout(save_layout)

        menu_widget = QtWidgets.QWidget()
        menu_widget.setLayout(menu)
        menu_widget.setFixedWidth(320)

        histogram_layout = QtWidgets.QVBoxLayout()
        histogram_layout.addWidget(self.image_label)
        histogram_layout.addWidget(self.coeff_label)

        window = QtWidgets.QHBoxLayout()
        window.setAlignment(QtCore.Qt.AlignLeft)
        window.addWidget(menu_widget)
        window.addLayout(histogram_layout)

        self.setLayout(window)
        self.setWindowTitle(self.appname)
        self.show()
