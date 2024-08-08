from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class AnimatedLineEdit(QLineEdit):

    def __init__(self, placeholderText, parent=None):
        super(AnimatedLineEdit, self).__init__(parent)

        self.placeholderText = placeholderText
        self.fontInner = QFont('Times', 11)
        self.fontOuter = QFont('Times', 9)
        self.fontCurrent = QFont(self.fontInner.family(), self.fontInner.pointSize())
        self.fontMetricsInner = QFontMetrics(self.fontInner)
        self.fontMetricsOuter = QFontMetrics(self.fontOuter)
        self.textInner = self.fontMetricsInner.boundingRect(self.placeholderText)
        self.textOuter = self.fontMetricsOuter.boundingRect(self.placeholderText)
        self.topOffset = int((self.textOuter.height() - 1) / 2)
        self.setContentsMargins(0, self.topOffset, 0, 0)
        self.positionInner = QPoint(10, self.height() - int((self.height() - self.textInner.height()) / 2))
        self.positionOuter = QPoint(10, int(self.textOuter.height() - self.topOffset / 2))
        self.positionCurrent = QPoint(self.positionInner.x(), self.positionInner.y())
        self.isPlaceholderInside = True

        self.timelinePositionOut = QTimeLine(150)
        self.timelinePositionOut.setFrameRange(self.positionCurrent.y(), self.positionOuter.y())
        self.timelinePositionOut.valueChanged.connect(self.timelinePositionOutValueChanged)

        self.timelinePositionIn = QTimeLine(150)
        self.timelinePositionIn.setFrameRange(self.positionCurrent.y(), self.positionInner.y())
        self.timelinePositionIn.valueChanged.connect(self.timelinePositionInValueChanged)

        self.timelineFontOut = QTimeLine(150)
        self.timelineFontOut.setFrameRange(self.fontCurrent.pointSize(), self.fontOuter.pointSize())
        self.timelineFontOut.valueChanged.connect(self.timelineFontOutValueChanged)

        self.timelineFontIn = QTimeLine(150)
        self.timelineFontIn.setFrameRange(self.fontCurrent.pointSize(), self.fontInner.pointSize())
        self.timelineFontIn.valueChanged.connect(self.timelineFontInValueChanged)

    def timelinePositionOutValueChanged(self, value):
        self.positionCurrent.setY(int(self.positionCurrent.y() + (self.positionOuter.y() - self.positionCurrent.y()) * value))
        if value > 0.5 and self.isPlaceholderInside:
            self.isPlaceholderInside = False
        self.update()

    def timelinePositionInValueChanged(self, value):
        self.positionCurrent.setY(int(self.positionCurrent.y() + (self.positionInner.y() - self.positionCurrent.y()) * value))
        if value > 0.5 and not self.isPlaceholderInside:
            self.isPlaceholderInside = True
        self.update()

    def timelineFontOutValueChanged(self, value):
        self.fontCurrent.setPointSize(int(self.fontCurrent.pointSize() - (self.fontCurrent.pointSize() - self.fontOuter.pointSize()) * value))
        self.update()

    def timelineFontInValueChanged(self, value):
        self.fontCurrent.setPointSize(int(self.fontCurrent.pointSize() - (self.fontCurrent.pointSize() - self.fontInner.pointSize()) * value))
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setFont(self.fontCurrent)

        if not self.isPlaceholderInside:
            painter.setPen(QColor(255, 255, 255))
            painter.drawLine(QPoint(5, self.topOffset), QPoint(self.textOuter.width() + 15, self.topOffset))

        if not self.hasFocus() and not self.text():
            painter.setPen(QColor(100, 100, 100))
            painter.drawText(self.positionCurrent, self.placeholderText)
        else:
            painter.setPen(QColor(100, 100, 100))
            painter.drawText(self.positionCurrent, self.placeholderText)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        if not self.text():
            self.timelinePositionIn.stop()
            self.timelineFontIn.stop()
            self.timelinePositionOut.start()
            self.timelineFontOut.start()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        if not self.text():
            self.timelinePositionOut.stop()
            self.timelineFontOut.stop()
            self.timelinePositionIn.start()
            self.timelineFontIn.start()

    def setPlaceholderText(self, placeholderText):
        self.placeholderText = placeholderText
