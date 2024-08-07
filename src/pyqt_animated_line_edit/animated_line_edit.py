from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class AnimatedLineEdit(QLineEdit):

    def __init__(self, placeholderText, parent=None):
        super(AnimatedLineEdit, self).__init__(parent)
        self.placeholderText = placeholderText

    def setPlaceholderText(self, placeholderText):
        self.placeholderText = placeholderText
