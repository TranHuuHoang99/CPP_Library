import ctypes
import numpy as np
from PIL import Image as im
import random as rand
import pickle
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets
import sys
import math
from typing import overload
import os

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.show()
    app.exec()