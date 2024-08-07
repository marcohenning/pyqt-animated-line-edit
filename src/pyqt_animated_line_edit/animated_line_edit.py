from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class AnimatedLineEdit(QLineEdit):

    def __init__(self, placeholderText, parent=None):
        super(AnimatedLineEdit, self).__init__(parent)

        self.placeholderText = placeholderText
        self.font = QFont('Times', 10)
        self.setContentsMargins(0, 5, 0, 0)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setFont(self.font)
        painter.setPen(QColor(100, 100, 100))

        if not self.hasFocus():
            painter.drawText(10, 25, self.placeholderText)
        else:
            painter.drawText(10, 5, self.placeholderText)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        print('focusInEvent')

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        print('focusOutEvent')

    def setPlaceholderText(self, placeholderText):
        self.placeholderText = placeholderText
