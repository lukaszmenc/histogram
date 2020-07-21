from PyQt5 import QtWidgets
from .data_operations import prepare_data, histogram


def create_histogram(df, column_object, lsl, usl):
    try:
        column_name = [item.text() for item in column_object][0]
        data = prepare_data(df, column_name)
        print(data)
        chart = histogram(data, column_name, lsl, usl)
        print(chart)
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
