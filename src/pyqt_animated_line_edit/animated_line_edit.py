import math
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class AnimatedLineEdit(QLineEdit):

    def __init__(self, placeholder_text, parent=None):
        super(AnimatedLineEdit, self).__init__(parent)

        self.__placeholder_text = placeholder_text
        self.__color = QColor(0, 0, 0)
        self.__placeholder_color = QColor(100, 100, 100)
        self.__placeholder_color_outside = None
        self.__placeholder_color_current = self.__placeholder_color
        self.__background_color = QColor(255, 255, 255)
        self.__border_color = QColor(0, 0, 0)
        self.__border_width = 1
        self.__border_radius = 0
        self.__placeholder_text_start = max(15, self.__border_radius + 10)
        self.__font_inner = self.font()
        self.__font_outer = self.font()
        self.__font_current = QFont(self.__font_inner.family(), self.__font_inner.pointSize())

        self.__is_placeholder_inside = True
        self.__easing_curve = QEasingCurve.Type.InOutCubic
        self.__duration = 150
        self.__padding = [0, 0, 0, 0]
        self.__hovered_color = None
        self.__hovered_background_color = None
        self.__hovered_border_color = None
        self.__hovered_border_width = None
        self.__focused_color = None
        self.__focused_background_color = None
        self.__focused_border_color = self.palette().color(QPalette.ColorRole.Highlight)
        self.__focused_border_width = None
        self.__disabled_color = None
        self.__disabled_background_color = None
        self.__disabled_border_color = None
        self.__disabled_border_width = None

        self.__calculate_geometry()
        self.__update_style_sheet()

        self.__timeline_position_out = QTimeLine(self.__duration)
        self.__timeline_position_out.setFrameRange(self.__position_current.y(), self.__position_outer.y())
        self.__timeline_position_out.setEasingCurve(self.__easing_curve)
        self.__timeline_position_out.valueChanged.connect(self.__timeline_position_out_value_changed)

        self.__timeline_position_in = QTimeLine(self.__duration)
        self.__timeline_position_in.setFrameRange(self.__position_current.y(), self.__position_inner.y())
        self.__timeline_position_in.setEasingCurve(self.__easing_curve)
        self.__timeline_position_in.valueChanged.connect(self.__timeline_position_in_value_changed)

        self.__timeline_font_out = QTimeLine(self.__duration)
        self.__timeline_font_out.setFrameRange(self.__font_current.pointSize(), self.__font_outer.pointSize())
        self.__timeline_font_out.setEasingCurve(self.__easing_curve)
        self.__timeline_font_out.valueChanged.connect(self.__timeline_font_out_value_changed)

        self.__timeline_font_in = QTimeLine(self.__duration)
        self.__timeline_font_in.setFrameRange(self.__font_current.pointSize(), self.__font_inner.pointSize())
        self.__timeline_font_in.setEasingCurve(self.__easing_curve)
        self.__timeline_font_in.valueChanged.connect(self.__timeline_font_in_value_changed)

        self.__timeline_position_start = 0
        self.__timeline_font_start = 0

    def __timeline_position_out_value_changed(self, value):
        self.__position_current.setY(math.floor(self.__timeline_position_start + (self.__position_outer.y() - self.__timeline_position_start) * value))

        if value > 0.2 and self.__is_placeholder_inside:
            self.__is_placeholder_inside = False
            self.__placeholder_color_current = self.__placeholder_color_outside if self.__placeholder_color_outside is not None else self.__placeholder_color

        self.update()

    def __timeline_position_in_value_changed(self, value):
        self.__position_current.setY(math.ceil(self.__timeline_position_start + (self.__position_inner.y() - self.__timeline_position_start) * value))

        if value > 0.2 and not self.__is_placeholder_inside:
            self.__is_placeholder_inside = True
            self.__placeholder_color_current = self.__placeholder_color

        self.update()

    def __timeline_font_out_value_changed(self, value):
        self.__font_current.setPointSize(math.floor(self.__timeline_font_start + (self.__font_outer.pointSize() - self.__timeline_font_start) * value))
        self.update()

    def __timeline_font_in_value_changed(self, value):
        self.__font_current.setPointSize(math.ceil(self.__timeline_font_start + (self.__font_inner.pointSize() - self.__timeline_font_start) * value))
        self.update()

    def __calculate_geometry(self):
        self.__font_metrics_inner = QFontMetrics(self.__font_inner)
        self.__font_metrics_outer = QFontMetrics(self.__font_outer)
        self.__text_inner_rect = self.__font_metrics_inner.tightBoundingRect(self.__placeholder_text)
        self.__text_outer_rect = self.__font_metrics_outer.tightBoundingRect(self.__placeholder_text)
        self.__top_offset = math.ceil((self.__text_outer_rect.height() - (self.__border_width if self.__focused_border_width is None else self.__focused_border_width)) / 2)
        self.setContentsMargins(0, self.__top_offset, 0, 0)
        self.__position_inner = QPoint(self.__placeholder_text_start, self.__top_offset + (self.height() - self.__top_offset - math.ceil((self.height() - self.__top_offset - self.__text_inner_rect.height()) / 2)))
        self.__position_outer = QPoint(self.__placeholder_text_start, self.__text_outer_rect.height())
        self.__position_current = QPoint(self.__position_inner.x(), self.__position_inner.y())

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setFont(self.__font_current)

        if not self.__is_placeholder_inside:
            painter.setPen(self.__background_color)
            for i in range(self.__border_width if self.__focused_border_width is None else self.__focused_border_width):
                painter.drawLine(QPoint(self.__placeholder_text_start - 5, self.__top_offset + i),
                                 QPoint(self.__placeholder_text_start + self.__text_outer_rect.width() + 5, self.__top_offset + i))

        painter.setPen(self.__placeholder_color_current)
        painter.drawText(self.__position_current, self.__placeholder_text)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        if not self.text():
            self.__timeline_position_in.stop()
            self.__timeline_font_in.stop()
            self.__timeline_position_start = self.__position_current.y()
            self.__timeline_font_start = self.__font_current.pointSize()
            self.__timeline_position_out.start()
            self.__timeline_font_out.start()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        if not self.text():
            self.__timeline_position_out.stop()
            self.__timeline_font_out.stop()
            self.__timeline_position_start = self.__position_current.y()
            self.__timeline_font_start = self.__font_current.pointSize()
            self.__timeline_position_in.start()
            self.__timeline_font_in.start()

    def resizeEvent(self, event):
        self.__calculate_geometry()

    def __update_style_sheet(self):
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
                           % (self.__color.name(),
                              self.__background_color.name(),
                              self.__border_width,
                              self.__border_color.name(),
                              self.__border_radius,
                              self.__padding[0],
                              self.__padding[1],
                              self.__padding[2],
                              self.__padding[3],
                              self.__color.name() if self.__hovered_color is None else self.__hovered_color.name(),
                              self.__background_color.name() if self.__hovered_background_color is None else self.__hovered_background_color.name(),
                              self.__border_width if self.__hovered_border_width is None else self.__hovered_border_width,
                              self.__border_color.name() if self.__hovered_border_color is None else self.__hovered_border_color.name(),
                              self.__color.name() if self.__focused_color is None else self.__focused_color.name(),
                              self.__background_color.name() if self.__focused_background_color is None else self.__focused_background_color.name(),
                              self.__border_width if self.__focused_border_width is None else self.__focused_border_width,
                              self.__border_color.name() if self.__focused_border_color is None else self.__focused_border_color.name(),
                              self.__color.name() if self.__disabled_color is None else self.__disabled_color.name(),
                              self.__background_color.name() if self.__disabled_background_color is None else self.__disabled_background_color.name(),
                              self.__border_width if self.__disabled_border_width is None else self.__disabled_border_width,
                              self.__border_color.name() if self.__disabled_border_color is None else self.__disabled_border_color.name()))

    def getPlaceholderText(self):
        return self.__placeholder_text

    def setPlaceholderText(self, text):
        self.__placeholder_text = text

    def getColor(self):
        return self.__color

    def setColor(self, color):
        self.__color = color
        self.__update_style_sheet()

    def getPlaceholderColor(self):
        return self.__placeholder_color

    def setPlaceholderColor(self, color):
        self.__placeholder_color = color

    def getPlaceholderColorOutside(self):
        return self.__placeholder_color_outside

    def setPlaceholderColorOutside(self, color):
        self.__placeholder_color_outside = color

    def getBackgroundColor(self):
        return self.__background_color

    def setBackgroundColor(self, color):
        self.__background_color = color
        self.__update_style_sheet()

    def getBorderColor(self):
        return self.__border_color

    def setBorderColor(self, color):
        self.__border_color = color
        self.__update_style_sheet()

    def getBorderWidth(self):
        return self.__border_width

    def setBorderWidth(self, width):
        self.__border_width = width
        self.__update_style_sheet()

    def getBorderRadius(self):
        return self.__border_radius

    def setBorderRadius(self, radius):
        self.__border_radius = radius
        self.__update_style_sheet()
        self.__placeholder_text_start = max(15, self.__border_radius + 10)

    def getFontInner(self):
        return self.__font_inner

    def getFontOuter(self):
        return self.__font_outer

    def setFontFamily(self, family):
        self.__font_inner.setFamily(family)
        self.__font_outer.setFamily(family)
        self.__font_current = QFont(self.__font_inner.family(), self.__font_inner.pointSize())
        self.__font_current.setWeight(self.__font_inner.weight())
        self.__font_current.setItalic(self.__font_inner.italic())
        self.__calculate_geometry()

    def setFontSizeInner(self, size):
        self.__font_inner.setPointSize(size)
        self.__font_current = QFont(self.__font_inner.family(), self.__font_inner.pointSize())
        self.__font_current.setWeight(self.__font_inner.weight())
        self.__font_current.setItalic(self.__font_inner.italic())
        self.__calculate_geometry()

    def setFontSizeOuter(self, size):
        self.__font_outer.setPointSize(size)
        self.__calculate_geometry()

    def setPlaceholderFontBold(self, enable):
        self.__font_inner.setBold(enable)
        self.__font_outer.setBold(enable)
        self.__font_current.setBold(enable)
        self.__calculate_geometry()

    def setPlaceholderFontItalic(self, enable):
        self.__font_inner.setItalic(enable)
        self.__font_outer.setItalic(enable)
        self.__font_current.setItalic(enable)
        self.__calculate_geometry()

    def getPadding(self):
        return self.__padding

    def setPadding(self, top, right, bottom, left):
        self.__padding = [top, right, bottom, left]
        self.__update_style_sheet()

    def getDuration(self):
        return self.__duration

    def setDuration(self, duration):
        self.__duration = duration
        self.__timeline_position_in.setDuration(self.__duration)
        self.__timeline_position_out.setDuration(self.__duration)
        self.__timeline_font_in.setDuration(self.__duration)
        self.__timeline_font_out.setDuration(self.__duration)

    def getEasingCurve(self):
        return self.__easing_curve

    def setEasingCurve(self, easingCurve):
        self.__easing_curve = easingCurve
        self.__timeline_position_in.setEasingCurve(self.__easing_curve)
        self.__timeline_position_out.setEasingCurve(self.__easing_curve)
        self.__timeline_font_in.setEasingCurve(self.__easing_curve)
        self.__timeline_font_out.setEasingCurve(self.__easing_curve)

    def getHoveredColor(self):
        return self.__hovered_color

    def setHoveredColor(self, color):
        self.__hovered_color = color
        self.__update_style_sheet()

    def getHoveredBackgroundColor(self):
        return self.__hovered_background_color

    def setHoveredBackgroundColor(self, color):
        self.__hovered_background_color = color
        self.__update_style_sheet()

    def getHoveredBorderColor(self):
        return self.__hovered_border_color

    def setHoveredBorderColor(self, color):
        self.__hovered_border_color = color
        self.__update_style_sheet()

    def getHoveredBorderWidth(self):
        return self.__hovered_border_width

    def setHoveredBorderWidth(self, width):
        self.__hovered_border_width = width
        self.__update_style_sheet()

    def getFocusedColor(self):
        return self.__focused_color

    def setFocusedColor(self, color):
        self.__focused_color = color
        self.__update_style_sheet()

    def getFocusedBackgroundColor(self):
        return self.__focused_background_color

    def setFocusedBackgroundColor(self, color):
        self.__focused_background_color = color
        self.__update_style_sheet()

    def getFocusedBorderColor(self):
        return self.__focused_border_color

    def setFocusedBorderColor(self, color):
        self.__focused_border_color = color
        self.__update_style_sheet()

    def getFocusedBorderWidth(self):
        return self.__focused_border_width

    def setFocusedBorderWidth(self, width):
        self.__focused_border_width = width
        self.__update_style_sheet()

    def getDisabledColor(self):
        return self.__disabled_color

    def setDisabledColor(self, color):
        self.__disabled_color = color
        self.__update_style_sheet()

    def getDisabledBackgroundColor(self):
        return self.__disabled_background_color

    def setDisabledBackgroundColor(self, color):
        self.__disabled_background_color = color
        self.__update_style_sheet()

    def getDisabledBorderColor(self):
        return self.__disabled_border_color

    def setDisabledBorderColor(self, color):
        self.__disabled_border_color = color
        self.__update_style_sheet()

    def getDisabledBorderWidth(self):
        return self.__disabled_border_width

    def setDisabledBorderWidth(self, width):
        self.__disabled_border_width = width
        self.__update_style_sheet()
