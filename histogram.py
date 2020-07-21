#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication
from scripts.interface import Interface


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Interface()
    sys.exit(app.exec_())
