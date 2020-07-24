from PyQt5 import QtWidgets, QtGui
from .data_operations import prepare_data, histogram
from PIL.ImageQt import ImageQt
from PIL import Image


def set_image(label, image):
    image = Image.open(image)
    pixmap = QtGui.QPixmap.fromImage(ImageQt(image))
    label.setPixmap(pixmap)


def set_coeff(label, data):
    if data:
        label.setText(
                f"\n\n\nCp: {data['Cp']}\n"
                f"CPU: {data['CPU']}\n"
                f"CPL: {data['CPL']}\n"
                f"Cpk: {data['Cpk']}\n"
                f"µ: {data['mu']}\n"
                f"σ: {data['sigma']}\n"
                f"min: {data['min']}\n"
                f"max: {data['max']}\n"
                f"ω: {data['dominant']}"
            )
    else:
        label.setText('No data')


def create_histogram(df, column_object, lsl, usl, output, image_label, coeff_label):
    try:
        column_name = [item.text() for item in column_object][0]
        data = prepare_data(df, column_name)
        chart, coeffs = histogram(data, column_name, float(lsl), float(usl))

        output = {'histogram': chart, 'data': coeffs}

        set_image(image_label, output['histogram'])
        set_coeff(coeff_label, output['data'])

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
