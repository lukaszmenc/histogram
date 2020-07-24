from PyQt5 import QtGui
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





