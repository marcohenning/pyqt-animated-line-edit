from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class AnimatedLineEdit(QLineEdit):

    def __init__(self, placeholderText, parent=None):
        super(AnimatedLineEdit, self).__init__(parent)

        self.placeholderText = placeholderText
        self.fontInner = QFont('Times', 11)
        self.fontOuter = QFont('Times', 9)
        self.fontMetricsInner = QFontMetrics(self.fontInner)
        self.fontMetricsOuter = QFontMetrics(self.fontOuter)
        self.textInner = self.fontMetricsInner.boundingRect(self.placeholderText)
        self.textOuter = self.fontMetricsOuter.boundingRect(self.placeholderText)
        self.topOffset = int((self.textOuter.height() - 1) / 2)
        self.setContentsMargins(0, self.topOffset, 0, 0)
        self.positionInner = QPoint(10, self.height() - int((self.height() - self.textInner.height()) / 2))
        self.positionOuter = QPoint(10, int(self.textOuter.height() - self.topOffset / 2))

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        if not self.hasFocus():
            painter.setFont(self.fontInner)
            painter.setPen(QColor(100, 100, 100))
            painter.drawText(self.positionInner, self.placeholderText)
        else:
            painter.setFont(self.fontOuter)
            painter.setPen(QColor(255, 255, 255))
            painter.drawLine(QPoint(5, self.topOffset), QPoint(self.textOuter.width() + 15, self.topOffset))
            painter.setPen(QColor(100, 100, 100))
            painter.drawText(self.positionOuter, self.placeholderText)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        print('focusInEvent')

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        print('focusOutEvent')

    def setPlaceholderText(self, placeholderText):
        self.placeholderText = placeholderText
