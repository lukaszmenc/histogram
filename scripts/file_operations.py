import os
import pandas as pd
from PyQt5 import QtWidgets


def get_file_path():
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
        None, "Wybór pliku", os.path.expanduser("~/Desktop"), "CSV (*.csv)",
    )
    return file_path


def get_data_from_csv(path):
    return pd.read_csv(path)

