import math
from qtpy.QtGui import QColor, QFont, QPalette, QPainter, QFontMetrics
from qtpy.QtCore import QEasingCurve, QTimeLine, QPoint, Qt, QMargins
from qtpy.QtWidgets import QLineEdit


class AnimatedLineEdit(QLineEdit):

    def __init__(self, placeholder_text, parent=None):
        """Creates a new AnimatedLineEdit instance

        :param placeholder_text: the displayed placeholder text
        :param parent: the parent widget
        """

        super(AnimatedLineEdit, self).__init__(parent)

        # Placeholder text
        self.__placeholder_text = placeholder_text
        self.__placeholder_text_current = self.__placeholder_text
        self.__is_placeholder_inside = True

        # Font settings
        self.__placeholder_font_inner = self.font()
        self.__placeholder_font_outer = self.font()
        self.__placeholder_font_current = QFont(self.__placeholder_font_inner.family(),
                                                self.__placeholder_font_inner.pointSize())

        # Animation settings
        self.__transition_duration = 250
        self.__transition_easing_curve = QEasingCurve.Type.InOutCubic

        # Styling settings
        self.__color = QColor(0, 0, 0)
        self.__background_color = QColor(255, 255, 255)
        self.__border_color = self.palette().color(QPalette.ColorRole.Shadow)
        self.__placeholder_color = self.palette().color(QPalette.ColorRole.Shadow)
        self.__placeholder_color_outside = None
        self.__placeholder_color_current = self.__placeholder_color
        self.__border_width = 1
        self.__border_radius = 0
        self.__padding = QMargins()
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

        # Calculate widget geometry and update stylesheet
        self.__calculate_geometry()
        self.__update_style_sheet()

        # Timeline starting values necessary for interpolation
        self.__timeline_position_start = 0
        self.__timeline_font_start = 0

        # Timeline for moving the placeholder text to the outside position
        self.__timeline_position_out = QTimeLine(self.__transition_duration)
        self.__timeline_position_out.setFrameRange(self.__position_current.y(), self.__position_outer.y())
        self.__timeline_position_out.setEasingCurve(self.__transition_easing_curve)
        self.__timeline_position_out.valueChanged.connect(self.__timeline_position_out_value_changed)

        # Timeline for moving the placeholder text to the inside position
        self.__timeline_position_in = QTimeLine(self.__transition_duration)
        self.__timeline_position_in.setFrameRange(self.__position_current.y(), self.__position_inner.y())
        self.__timeline_position_in.setEasingCurve(self.__transition_easing_curve)
        self.__timeline_position_in.valueChanged.connect(self.__timeline_position_in_value_changed)

        # Timeline for scaling the font to the outside font size
        self.__timeline_font_out = QTimeLine(self.__transition_duration)
        self.__timeline_font_out.setFrameRange(self.__placeholder_font_current.pointSize(),
                                               self.__placeholder_font_outer.pointSize())
        self.__timeline_font_out.setEasingCurve(self.__transition_easing_curve)
        self.__timeline_font_out.valueChanged.connect(self.__timeline_font_out_value_changed)

        # Timeline for scaling the font to the inside font size
        self.__timeline_font_in = QTimeLine(self.__transition_duration)
        self.__timeline_font_in.setFrameRange(self.__placeholder_font_current.pointSize(),
                                              self.__placeholder_font_inner.pointSize())
        self.__timeline_font_in.setEasingCurve(self.__transition_easing_curve)
        self.__timeline_font_in.valueChanged.connect(self.__timeline_font_in_value_changed)


    def __timeline_position_out_value_changed(self, value):
        """Method that gets called every time the timeline's value changes.
        Calculates the new placeholder text position and forces the widget to update.

        :param value: current timeline value (between 0.0 and 1.0)
        """

        self.__position_current.setY(
            math.floor(self.__timeline_position_start +
                       (self.__position_outer.y() - self.__timeline_position_start) * value))

        if value > 0.1 and self.__is_placeholder_inside:
            self.__is_placeholder_inside = False

        self.update()

    def __timeline_position_in_value_changed(self, value):
        """Method that gets called every time the timeline's value changes.
        Calculates the new placeholder text position and forces the widget to update.

        :param value: current timeline value (between 0.0 and 1.0)
        """

        self.__position_current.setY(
            math.ceil(self.__timeline_position_start +
                      (self.__position_inner.y() - self.__timeline_position_start) * value))

        if value > 0.8 and not self.__is_placeholder_inside:
            self.__is_placeholder_inside = True

        self.update()

    def __timeline_font_out_value_changed(self, value):
        """Method that gets called every time the timeline's value changes.
        Calculates the new placeholder text font size and forces the widget to update.

        :param value: current timeline value (between 0.0 and 1.0)
        """

        self.__placeholder_font_current.setPointSize(
            math.floor(self.__timeline_font_start +
                       (self.__placeholder_font_outer.pointSize() - self.__timeline_font_start) * value))

        if self.__placeholder_font_current.pointSize() == self.__placeholder_font_outer.pointSize() and \
                self.__placeholder_text_current != self.__placeholder_text_outer_elided:
            self.__placeholder_text_current = self.__placeholder_text_outer_elided

        self.update()

    def __timeline_font_in_value_changed(self, value):
        """Method that gets called every time the timeline's value changes.
        Calculates the new placeholder text font size and forces the widget to update.

        :param value: current timeline value (between 0.0 and 1.0)
        """

        self.__placeholder_font_current.setPointSize(
            math.ceil(self.__timeline_font_start +
                      (self.__placeholder_font_inner.pointSize() - self.__timeline_font_start) * value))

        if self.__placeholder_font_current.pointSize() == self.__placeholder_font_inner.pointSize() and \
                self.__placeholder_text_current != self.__placeholder_text_inner_elided:
            self.__placeholder_text_current = self.__placeholder_text_inner_elided

        self.update()

    def __calculate_geometry(self):
        """Calculates everything related to widget geometry."""

        self.__font_metrics_inner = QFontMetrics(self.__placeholder_font_inner)
        self.__font_metrics_outer = QFontMetrics(self.__placeholder_font_outer)
        self.__placeholder_text_start = max(15, self.__border_radius + 10)

        self.__placeholder_text_inner_elided = self.__font_metrics_inner.elidedText(
            self.__placeholder_text, Qt.TextElideMode.ElideRight, self.width() - self.__placeholder_text_start * 2)
        self.__placeholder_text_outer_elided = self.__font_metrics_outer.elidedText(
            self.__placeholder_text, Qt.TextElideMode.ElideRight, self.width() - self.__placeholder_text_start * 2)

        self.__placeholder_text_current = self.__placeholder_text_inner_elided

        self.__text_inner_bounds = self.__font_metrics_inner.tightBoundingRect(self.__placeholder_text_inner_elided)
        self.__text_outer_bounds = self.__font_metrics_outer.tightBoundingRect(self.__placeholder_text_outer_elided)

        self.__top_offset = math.ceil(
            (self.__text_outer_bounds.height() -
             (self.__border_width if self.__focused_border_width is None else self.__focused_border_width)) / 2)

        self.setContentsMargins(0, self.__top_offset, 0, 0)

        self.__position_inner = QPoint(
            self.__placeholder_text_start,
            self.__top_offset + (self.height() - self.__top_offset - math.ceil(
                (self.height() - self.__top_offset - self.__text_inner_bounds.height()) / 2)))

        self.__position_outer = QPoint(self.__placeholder_text_start, self.__text_outer_bounds.height())
        self.__position_current = QPoint(self.__position_inner.x(), self.__position_inner.y())

    def paintEvent(self, event):
        """Method that gets called every time the widget needs to be updated.
        Everything related to widget graphics happens here.

        :param event: event sent by PyQt
        """

        super().paintEvent(event)
        painter = QPainter(self)
        painter.setFont(self.__placeholder_font_current)

        if not self.__is_placeholder_inside:
            painter.setPen(self.__background_color)
            for i in range(self.__border_width if self.__focused_border_width is None else self.__focused_border_width):
                painter.drawLine(QPoint(self.__placeholder_text_start - 5, self.__top_offset + i),
                                 QPoint(self.__placeholder_text_start + self.__text_outer_bounds.width() + 5,
                                        self.__top_offset + i))

        painter.setPen(self.__placeholder_color_current)
        painter.drawText(self.__position_current, self.__placeholder_text_current)

    def focusInEvent(self, event):
        """Method that gets called every time the widget gains focus.

        :param event: event sent by PyQt
        """

        super().focusInEvent(event)
        if not self.text():
            self.__timeline_position_in.stop()
            self.__timeline_font_in.stop()
            self.__timeline_position_start = self.__position_current.y()
            self.__timeline_font_start = self.__placeholder_font_current.pointSize()

            if len(self.__placeholder_text_outer_elided) <= len(self.__placeholder_text_inner_elided):
                self.__placeholder_text_current = self.__placeholder_text_outer_elided

            self.__placeholder_color_current = (self.__placeholder_color_outside if
                                                self.__placeholder_color_outside is not None
                                                else self.__placeholder_color)
            self.__timeline_position_out.start()
            self.__timeline_font_out.start()

    def focusOutEvent(self, event):
        """Method that gets called every time the widget loses focus.

        :param event: event sent by PyQt
        """

        super().focusOutEvent(event)
        if not self.text():
            self.__timeline_position_out.stop()
            self.__timeline_font_out.stop()
            self.__timeline_position_start = self.__position_current.y()
            self.__timeline_font_start = self.__placeholder_font_current.pointSize()

            if len(self.__placeholder_text_inner_elided) <= len(self.__placeholder_text_outer_elided):
                self.__placeholder_text_current = self.__placeholder_text_inner_elided

            self.__placeholder_color_current = self.__placeholder_color
            self.__timeline_position_in.start()
            self.__timeline_font_in.start()

    def resizeEvent(self, event):
        """Method that gets called every time the widget is resized.

        :param event: event sent by PyQt
        """

        self.__calculate_geometry()

    def __update_style_sheet(self):
        """Updates the stylesheet according to the current values."""

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
                              self.__padding.top(),
                              self.__padding.right(),
                              self.__padding.bottom(),
                              self.__padding.left(),
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

    def getPlaceholderText(self) -> str:
        """Get the current placeholder text

        :return: placeholder text
        """

        return self.__placeholder_text

    def setPlaceholderText(self, text: str):
        """Set the placeholder text

        :param text: new placeholder text
        """

        self.__placeholder_text = text

    def getColor(self) -> QColor:
        """Get the current text color

        :return: text color
        """

        return self.__color

    def setColor(self, color: QColor):
        """Set the text color

        :param color: new text color
        """

        self.__color = color
        self.__update_style_sheet()

    def getPlaceholderColor(self) -> QColor:
        """Get the current placeholder text color

        :return: placeholder text color
        """

        return self.__placeholder_color

    def setPlaceholderColor(self, color: QColor):
        """Set the placeholder text color

        :param color: new placeholder text color
        """

        self.__placeholder_color = color

    def getPlaceholderColorOutside(self) -> QColor:
        """Get the current placeholder text color for the outside position.
        If this is not set the color for the inside position will be used

        :return: placeholder text color for the outside position
        """

        return self.__placeholder_color_outside

    def setPlaceholderColorOutside(self, color: QColor):
        """Set the placeholder text color for the outside position

        :param color: new placeholder text color for the outside position
        """

        self.__placeholder_color_outside = color

    def getBackgroundColor(self) -> QColor:
        """Get the current background color

        :return: background color
        """

        return self.__background_color

    def setBackgroundColor(self, color: QColor):
        """Set the background color

        :param color: new background color
        """

        self.__background_color = color
        self.__update_style_sheet()

    def getBorderColor(self) -> QColor:
        """Get the current border color

        :return: border color
        """

        return self.__border_color

    def setBorderColor(self, color: QColor):
        """Set the border color

        :param color: new border color
        """

        self.__border_color = color
        self.__update_style_sheet()

    def getBorderWidth(self) -> int:
        """Get the current border width

        :return: border width
        """

        return self.__border_width

    def setBorderWidth(self, width: int):
        """Set the border width

        :param width: new border width
        """

        self.__border_width = width
        self.__update_style_sheet()

    def getBorderRadius(self) -> int:
        """Get the current border radius

        :return: border radius
        """

        return self.__border_radius

    def setBorderRadius(self, radius: int):
        """Set the border radius

        :param radius: new border radius
        """

        self.__border_radius = radius
        self.__update_style_sheet()
        self.__placeholder_text_start = max(15, self.__border_radius + 10)

    def getPlaceholderFontInner(self) -> QFont:
        """Get the current placeholder text font for the inside position

        :return: placeholder text font for the inside position
        """

        return self.__placeholder_font_inner

    def getPlaceholderFontOuter(self) -> QFont:
        """Get the current placeholder text font for the outside position

        :return: placeholder text font for the outside position
        """

        return self.__placeholder_font_outer

    def setPlaceholderFontFamily(self, family: str):
        """Set the font family of the placeholder text for all positions

        :param family: new font family of the placeholder text
        """

        self.__placeholder_font_inner.setFamily(family)
        self.__placeholder_font_outer.setFamily(family)
        self.__placeholder_font_current = QFont(self.__placeholder_font_inner.family(),
                                                self.__placeholder_font_inner.pointSize())
        self.__placeholder_font_current.setWeight(self.__placeholder_font_inner.weight())
        self.__placeholder_font_current.setItalic(self.__placeholder_font_inner.italic())
        self.__calculate_geometry()

    def setPlaceholderFontSizeInner(self, size: int):
        """Set the placeholder text font size for the inside position

        :param size: new placeholder text font size for the inside position
        """

        self.__placeholder_font_inner.setPointSize(size)
        self.__placeholder_font_current = QFont(self.__placeholder_font_inner.family(),
                                                self.__placeholder_font_inner.pointSize())
        self.__placeholder_font_current.setWeight(self.__placeholder_font_inner.weight())
        self.__placeholder_font_current.setItalic(self.__placeholder_font_inner.italic())
        self.__calculate_geometry()

    def setPlaceholderFontSizeOuter(self, size: int):
        """Set the placeholder text font size for the outside position

        :param size: new placeholder text font size for the outside position
        """

        self.__placeholder_font_outer.setPointSize(size)
        self.__calculate_geometry()

    def setPlaceholderFontBold(self, enable: bool):
        """Set whether the placeholder text font should be bold

        :param enable: whether the placeholder text font should be bold
        """

        self.__placeholder_font_inner.setBold(enable)
        self.__placeholder_font_outer.setBold(enable)
        self.__placeholder_font_current.setBold(enable)
        self.__calculate_geometry()

    def setPlaceholderFontItalic(self, enable: bool):
        """Set whether the placeholder text font should be italic

        :param enable: whether the placeholder text font should be italic
        """

        self.__placeholder_font_inner.setItalic(enable)
        self.__placeholder_font_outer.setItalic(enable)
        self.__placeholder_font_current.setItalic(enable)
        self.__calculate_geometry()

    def getPadding(self) -> QMargins:
        """Get the current padding of the widget

        :return: current padding
        """

        return self.__padding

    def setPadding(self, padding: QMargins):
        """Set the padding of the widget

        :param padding: padding of the widget
        """

        self.__padding = padding
        self.__update_style_sheet()

    def getTransitionDuration(self) -> int:
        """Get the current transition duration of the placeholder text

        :return: transition duration of the placeholder text
        """

        return self.__transition_duration

    def setTransitionDuration(self, duration: int):
        """Set the transition duration of the placeholder text

        :param duration: new transition duration of the placeholder text
        """

        self.__transition_duration = duration
        self.__timeline_position_in.setDuration(self.__transition_duration)
        self.__timeline_position_out.setDuration(self.__transition_duration)
        self.__timeline_font_in.setDuration(self.__transition_duration)
        self.__timeline_font_out.setDuration(self.__transition_duration)

    def getEasingCurve(self) -> QEasingCurve.Type:
        """Get the current easing curve used for the placeholder text transition

        :return: easing curve used for the placeholder text transition
        """

        return self.__transition_easing_curve

    def setEasingCurve(self, easing_curve: QEasingCurve.Type):
        """Set the easing curve used for the placeholder text transition

        :param easing_curve: new easing curve used for the placeholder text transition
        """

        self.__transition_easing_curve = easing_curve
        self.__timeline_position_in.setEasingCurve(self.__transition_easing_curve)
        self.__timeline_position_out.setEasingCurve(self.__transition_easing_curve)
        self.__timeline_font_in.setEasingCurve(self.__transition_easing_curve)
        self.__timeline_font_out.setEasingCurve(self.__transition_easing_curve)

    def getHoveredColor(self) -> QColor:
        """Get the current hovered text color

        :return: hovered text color
        """

        return self.__hovered_color

    def setHoveredColor(self, color: QColor):
        """Set the hovered text color

        :param color: new hovered text color
        """

        self.__hovered_color = color
        self.__update_style_sheet()

    def getHoveredBackgroundColor(self) -> QColor:
        """Get the current hovered background color

        :return: hovered background color
        """

        return self.__hovered_background_color

    def setHoveredBackgroundColor(self, color: QColor):
        """Set the hovered background color

        :param color: new hovered background color
        """

        self.__hovered_background_color = color
        self.__update_style_sheet()

    def getHoveredBorderColor(self) -> QColor:
        """Get the current hovered border color

        :return: hovered border color
        """

        return self.__hovered_border_color

    def setHoveredBorderColor(self, color: QColor):
        """Set the hovered border color

        :param color: new hovered border color
        """

        self.__hovered_border_color = color
        self.__update_style_sheet()

    def getHoveredBorderWidth(self) -> int:
        """Get the current hovered border width

        :return: hovered border width
        """

        return self.__hovered_border_width

    def setHoveredBorderWidth(self, width: int):
        """Set the hovered border width

        :param width: new hovered border width
        """

        self.__hovered_border_width = width
        self.__update_style_sheet()

    def getFocusedColor(self) -> QColor:
        """Get the current focused text color

        :return: focused text color
        """

        return self.__focused_color

    def setFocusedColor(self, color: QColor):
        """Set the focused text color

        :param color: new focused text color
        """

        self.__focused_color = color
        self.__update_style_sheet()

    def getFocusedBackgroundColor(self) -> QColor:
        """Get the current focused background color

        :return: focused background color
        """

        return self.__focused_background_color

    def setFocusedBackgroundColor(self, color: QColor):
        """Set the focused background color

        :param color: new focused background color
        """

        self.__focused_background_color = color
        self.__update_style_sheet()

    def getFocusedBorderColor(self) -> QColor:
        """Get the current focused border color

        :return: focused border color
        """

        return self.__focused_border_color

    def setFocusedBorderColor(self, color: QColor):
        """Set the focused border color

        :param color: new focused border color
        """

        self.__focused_border_color = color
        self.__update_style_sheet()

    def getFocusedBorderWidth(self) -> int:
        """Get the current focused border width

        :return: focused border width
        """

        return self.__focused_border_width

    def setFocusedBorderWidth(self, width: int):
        """Set the focused border width

        :param width: new focused border width
        """

        self.__focused_border_width = width
        self.__update_style_sheet()

    def getDisabledColor(self) -> QColor:
        """Get the current disabled text color

        :return: disabled text color
        """

        return self.__disabled_color

    def setDisabledColor(self, color: QColor):
        """Set the disabled text color

        :param color: new disabled text color
        """

        self.__disabled_color = color
        self.__update_style_sheet()

    def getDisabledBackgroundColor(self) -> QColor:
        """Get the current disabled background color

        :return: disabled background color
        """

        return self.__disabled_background_color

    def setDisabledBackgroundColor(self, color: QColor):
        """Set the disabled background color

        :param color: new disabled background color
        """

        self.__disabled_background_color = color
        self.__update_style_sheet()

    def getDisabledBorderColor(self) -> QColor:
        """Get the current disabled border color

        :return: disabled border color
        """

        return self.__disabled_border_color

    def setDisabledBorderColor(self, color: QColor):
        """Set the disabled border color

        :param color: new disabled border color
        """

        self.__disabled_border_color = color
        self.__update_style_sheet()

    def getDisabledBorderWidth(self) -> int:
        """Get the current disabled border width

        :return: disabled border width
        """

        return self.__disabled_border_width

    def setDisabledBorderWidth(self, width: int):
        """Set the disabled border width

        :param width: new disabled border width
        """

        self.__disabled_border_width = width
        self.__update_style_sheet()
