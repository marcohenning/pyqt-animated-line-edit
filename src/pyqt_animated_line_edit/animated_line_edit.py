from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class AnimatedLineEdit(QLineEdit):

    def __init__(self, placeholderText, parent=None):
        super(AnimatedLineEdit, self).__init__(parent)

        self.placeholderText = placeholderText
        self.color = QColor(0, 0, 0)
        self.placeholderColor = QColor(100, 100, 100)
        self.backgroundColor = QColor(255, 255, 255)
        self.borderColor = QColor(0, 0, 0)
        self.borderWidth = 1
        self.borderRadius = 0
        self.fontInner = QFont('Times', 11)
        self.fontOuter = QFont('Times', 9)
        self.fontCurrent = QFont(self.fontInner.family(), self.fontInner.pointSize())
        self.fontMetricsInner = QFontMetrics(self.fontInner)
        self.fontMetricsOuter = QFontMetrics(self.fontOuter)
        self.textInner = self.fontMetricsInner.boundingRect(self.placeholderText)
        self.textOuter = self.fontMetricsOuter.boundingRect(self.placeholderText)
        self.topOffset = int((self.textOuter.height() - 1) / 2)
        self.setContentsMargins(0, self.topOffset, 0, 0)
        self.placeholderTextStart = max(15, self.borderRadius + 10)
        self.positionInner = QPoint(self.placeholderTextStart, self.height() - int((self.height() - self.textInner.height()) / 2))
        self.positionOuter = QPoint(self.placeholderTextStart, int(self.textOuter.height() - self.topOffset / 2))
        self.positionCurrent = QPoint(self.positionInner.x(), self.positionInner.y())
        self.isPlaceholderInside = True
        self.easingCurve = QEasingCurve.Type.InOutCubic
        self.duration = 150
        self.padding = [0, 0, 0, 0]
        self.hoveredColor = None
        self.hoveredBackgroundColor = None
        self.hoveredBorderColor = None
        self.hoveredBorderWidth = None
        self.focussedColor = None
        self.focussedBackgroundColor = None
        self.focussedBorderColor = self.palette().color(QPalette.ColorRole.Highlight)
        self.focussedBorderWidth = None
        self.disabledColor = None
        self.disabledBackgroundColor = None
        self.disabledBorderColor = None
        self.disabledBorderWidth = None

        self.updateStyleSheet()

        self.timelinePositionOut = QTimeLine(self.duration)
        self.timelinePositionOut.setFrameRange(self.positionCurrent.y(), self.positionOuter.y())
        self.timelinePositionOut.setEasingCurve(self.easingCurve)
        self.timelinePositionOut.valueChanged.connect(self.timelinePositionOutValueChanged)

        self.timelinePositionIn = QTimeLine(self.duration)
        self.timelinePositionIn.setFrameRange(self.positionCurrent.y(), self.positionInner.y())
        self.timelinePositionIn.setEasingCurve(self.easingCurve)
        self.timelinePositionIn.valueChanged.connect(self.timelinePositionInValueChanged)

        self.timelineFontOut = QTimeLine(self.duration)
        self.timelineFontOut.setFrameRange(self.fontCurrent.pointSize(), self.fontOuter.pointSize())
        self.timelineFontOut.setEasingCurve(self.easingCurve)
        self.timelineFontOut.valueChanged.connect(self.timelineFontOutValueChanged)

        self.timelineFontIn = QTimeLine(self.duration)
        self.timelineFontIn.setFrameRange(self.fontCurrent.pointSize(), self.fontInner.pointSize())
        self.timelineFontIn.setEasingCurve(self.easingCurve)
        self.timelineFontIn.valueChanged.connect(self.timelineFontInValueChanged)

    def timelinePositionOutValueChanged(self, value):
        self.positionCurrent.setY(int(self.positionCurrent.y() + (self.positionOuter.y() - self.positionCurrent.y()) * value))
        if value > 0.2 and self.isPlaceholderInside:
            self.isPlaceholderInside = False
        self.update()

    def timelinePositionInValueChanged(self, value):
        self.positionCurrent.setY(int(self.positionCurrent.y() + (self.positionInner.y() - self.positionCurrent.y()) * value))
        if value > 0.2 and not self.isPlaceholderInside:
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
            painter.setPen(self.backgroundColor)
            for i in range(self.borderWidth):
                painter.drawLine(QPoint(self.placeholderTextStart - 5, self.topOffset + i),
                                 QPoint(self.placeholderTextStart + self.textOuter.width() + 5, self.topOffset + i))

        painter.setPen(self.placeholderColor)
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

    def updateStyleSheet(self):
        self.setStyleSheet('QLineEdit {'
                           'color: %s;'
                           'background-color: %s;'
                           'border: %dpx solid %s;'
                           'border-radius: %dpx;'
                           'padding: %d %d %d %dpx;'
                           '}'
                           'QLineEdit:hover {'
                           'color: %s;'
                           'background-color: %s;'
                           'border: %dpx solid %s;'
                           '}'
                           'QLineEdit:focus {'
                           'color: %s;'
                           'background-color: %s;'
                           'border: %dpx solid %s;'
                           '}'
                           'QLineEdit:disabled {'
                           'color: %s;'
                           'background-color: %s;'
                           'border: %dpx solid %s;'
                           '}'
                           % (self.color.name(),
                              self.backgroundColor.name(),
                              self.borderWidth,
                              self.borderColor.name(),
                              self.borderRadius,
                              self.padding[0],
                              self.padding[1],
                              self.padding[2],
                              self.padding[3],
                              self.color.name() if self.hoveredColor is None else self.hoveredColor.name(),
                              self.backgroundColor.name() if self.hoveredBackgroundColor is None else self.hoveredBackgroundColor.name(),
                              self.borderWidth if self.hoveredBorderWidth is None else self.hoveredBorderWidth,
                              self.borderColor.name() if self.hoveredBorderColor is None else self.hoveredBorderColor.name(),
                              self.color.name() if self.focussedColor is None else self.focussedColor.name(),
                              self.backgroundColor.name() if self.focussedBackgroundColor is None else self.focussedBackgroundColor.name(),
                              self.borderWidth if self.focussedBorderWidth is None else self.focussedBorderWidth,
                              self.borderColor.name() if self.focussedBorderColor is None else self.focussedBorderColor.name(),
                              self.color.name() if self.disabledColor is None else self.disabledColor.name(),
                              self.backgroundColor.name() if self.disabledBackgroundColor is None else self.disabledBackgroundColor.name(),
                              self.borderWidth if self.disabledBorderWidth is None else self.disabledBorderWidth,
                              self.borderColor.name() if self.disabledBorderColor is None else self.disabledBorderColor.name()))

    def getPlaceholderText(self):
        return self.placeholderText

    def setPlaceholderText(self, text):
        self.placeholderText = text

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color
        self.updateStyleSheet()

    def getPlaceholderColor(self):
        return self.placeholderColor

    def setPlaceholderColor(self, color):
        self.placeholderColor = color

    def getBackgroundColor(self):
        return self.backgroundColor

    def setBackgroundColor(self, color):
        self.backgroundColor = color
        self.updateStyleSheet()

    def getBorderColor(self):
        return self.borderColor

    def setBorderColor(self, color):
        self.borderColor = color
        self.updateStyleSheet()

    def getBorderWidth(self):
        return self.borderWidth

    def setBorderWidth(self, width):
        self.borderWidth = width
        self.updateStyleSheet()

    def getBorderRadius(self):
        return self.borderRadius

    def setBorderRadius(self, radius):
        self.borderRadius = radius
        self.updateStyleSheet()

    def getFontInner(self):
        return self.fontInner

    def getFontOuter(self):
        return self.fontOuter

    def setFontFamily(self, family):
        self.fontInner.setFamily(family)
        self.fontOuter.setFamily(family)
        self.fontCurrent = QFont(self.fontInner.family(), self.fontInner.pointSize())

    def setFontSizeInner(self, size):
        self.fontInner.setPointSize(size)
        self.fontCurrent = QFont(self.fontInner.family(), self.fontInner.pointSize())

    def setFontSizeOuter(self, size):
        self.fontOuter.setPointSize(size)

    def getPadding(self):
        return self.padding

    def setPadding(self, top, right, bottom, left):
        self.padding = [top, right, bottom, left]
        self.updateStyleSheet()

    def getDuration(self):
        return self.duration

    def setDuration(self, duration):
        self.duration = duration
        self.timelinePositionIn.setDuration(self.duration)
        self.timelinePositionOut.setDuration(self.duration)
        self.timelineFontIn.setDuration(self.duration)
        self.timelineFontOut.setDuration(self.duration)

    def getEasingCurve(self):
        return self.easingCurve

    def setEasingCurve(self, easingCurve):
        self.easingCurve = easingCurve

    def getHoveredColor(self):
        return self.hoveredColor

    def setHoveredColor(self, color):
        self.hoveredColor = color
        self.updateStyleSheet()

    def getHoveredBackgroundColor(self):
        return self.hoveredBackgroundColor

    def setHoveredBackgroundColor(self, color):
        self.hoveredBackgroundColor = color
        self.updateStyleSheet()

    def getHoveredBorderColor(self):
        return self.hoveredBorderColor

    def setHoveredBorderColor(self, color):
        self.hoveredBorderColor = color
        self.updateStyleSheet()

    def getHoveredBorderWidth(self):
        return self.hoveredBorderWidth

    def setHoveredBorderWidth(self, width):
        self.hoveredBorderWidth = width
        self.updateStyleSheet()

    def getFocussedColor(self):
        return self.focussedColor

    def setFocussedColor(self, color):
        self.focussedColor = color
        self.updateStyleSheet()

    def getFocussedBackgroundColor(self):
        return self.focussedBackgroundColor

    def setFocussedBackgroundColor(self, color):
        self.focussedBackgroundColor = color
        self.updateStyleSheet()

    def getFocussedBorderColor(self):
        return self.focussedBorderColor

    def setFocussedBorderColor(self, color):
        self.focussedBorderColor = color
        self.updateStyleSheet()

    def getFocussedBorderWidth(self):
        return self.focussedBorderWidth

    def setFocussedBorderWidth(self, width):
        self.focussedBorderWidth = width
        self.updateStyleSheet()

    def getDisabledColor(self):
        return self.disabledColor

    def setDisabledColor(self, color):
        self.disabledColor = color
        self.updateStyleSheet()

    def getDisabledBackgroundColor(self):
        return self.disabledBackgroundColor

    def setDisabledBackgroundColor(self, color):
        self.disabledBackgroundColor = color
        self.updateStyleSheet()

    def getDisabledBorderColor(self):
        return self.disabledBorderColor

    def setDisabledBorderColor(self, color):
        self.disabledBorderColor = color
        self.updateStyleSheet()

    def getDisabledBorderWidth(self):
        return self.disabledBorderWidth

    def setDisabledBorderWidth(self, width):
        self.disabledBorderWidth = width
        self.updateStyleSheet()
