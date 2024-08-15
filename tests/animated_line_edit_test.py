from PyQt6.QtGui import QColor, QPalette, QFont, QFocusEvent
from PyQt6.QtCore import QEasingCurve, QMargins
from PyQt6.QtTest import QTest
from pytestqt.qt_compat import qt_api
from src.pyqt_animated_line_edit.animated_line_edit import AnimatedLineEdit


def test_initial_values(qtbot):
    """Test initial values after instantiating"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    assert line_edit.getPlaceholderText() == 'Test'
    assert line_edit.isPlaceholderInside() == True
    assert line_edit.getPlaceholderFontInner() == line_edit.font()
    assert line_edit.getPlaceholderFontOuter() == line_edit.font()
    assert line_edit.getTransitionDuration() == 250
    assert line_edit.getEasingCurve() == QEasingCurve.Type.InOutCubic
    assert line_edit.getColor() == QColor(0, 0, 0)
    assert line_edit.getBackgroundColor() == QColor(255, 255, 255)
    assert line_edit.getBorderColor() == line_edit.palette().color(QPalette.ColorRole.Shadow)
    assert line_edit.getPlaceholderColor() == line_edit.palette().color(QPalette.ColorRole.Shadow)
    assert line_edit.getPlaceholderColorOutside() is None
    assert line_edit.getBorderWidth() == 1
    assert line_edit.getBorderRadius() == 0
    assert line_edit.getPadding() == QMargins()
    assert line_edit.getHoveredColor() is None
    assert line_edit.getHoveredBackgroundColor() is None
    assert line_edit.getHoveredBorderColor() is None
    assert line_edit.getHoveredBorderWidth() is None
    assert line_edit.getFocusedColor() is None
    assert line_edit.getFocusedBackgroundColor() is None
    assert line_edit.getFocusedBorderColor() == line_edit.palette().color(QPalette.ColorRole.Highlight)
    assert line_edit.getFocusedBorderWidth() is None
    assert line_edit.getDisabledColor() is None
    assert line_edit.getDisabledBackgroundColor() is None
    assert line_edit.getDisabledBorderColor() is None
    assert line_edit.getDisabledBorderWidth() is None

def test_set_placeholder_text(qtbot):
    """Test setting the placeholder text"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    line_edit.setPlaceholderText('Placeholder')

    assert line_edit.getPlaceholderText() == 'Placeholder'

def test_set_color(qtbot):
    """Test setting the text color"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    color = QColor(255, 0, 0)
    line_edit.setColor(color)

    assert line_edit.getColor() == color

def test_set_placeholder_color(qtbot):
    """Test setting the placeholder color"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    color = QColor(255, 0, 0)
    line_edit.setPlaceholderColor(color)

    assert line_edit.getPlaceholderColor() == color

def test_set_placeholder_color_outside(qtbot):
    """Test setting the placeholder color for the outside position"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    color = QColor(255, 0, 0)
    line_edit.setPlaceholderColorOutside(color)

    assert line_edit.getPlaceholderColorOutside() == color

def test_set_background_color(qtbot):
    """Test setting the background color"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    color = QColor(255, 0, 0)
    line_edit.setBackgroundColor(color)

    assert line_edit.getBackgroundColor() == color

def test_set_border_color(qtbot):
    """Test setting the border color"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    color = QColor(255, 0, 0)
    line_edit.setBorderColor(color)

    assert line_edit.getBorderColor() == color

def test_set_border_width(qtbot):
    """Test setting the border width"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    line_edit.setBorderWidth(10)

    assert line_edit.getBorderWidth() == 10

def test_set_border_radius(qtbot):
    """Test setting the border radius"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    line_edit.setBorderRadius(10)

    assert line_edit.getBorderRadius() == 10

def test_set_placeholder_font(qtbot):
    """Test getting the placeholder font for the inside position"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    font_family = 'Arial'
    font_size_inner = 20
    font_size_outer = 15
    is_bold = True
    is_italic = True

    font_inner = QFont(font_family, font_size_inner)
    font_inner.setBold(is_bold)
    font_inner.setItalic(is_italic)

    font_outer = QFont(font_family, font_size_outer)
    font_outer.setBold(is_bold)
    font_outer.setItalic(is_italic)

    line_edit.setPlaceholderFontFamily(font_family)
    line_edit.setPlaceholderFontSizeInner(font_size_inner)
    line_edit.setPlaceholderFontSizeOuter(font_size_outer)
    line_edit.setPlaceholderFontBold(is_bold)
    line_edit.setPlaceholderFontItalic(is_italic)

    assert line_edit.getPlaceholderFontInner() == font_inner
    assert line_edit.getPlaceholderFontOuter() == font_outer

def test_set_padding(qtbot):
    """Test setting the padding"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    padding = QMargins(10, 20, 30, 40)
    line_edit.setPadding(padding)

    assert line_edit.getPadding() == padding

def test_set_transition_duration(qtbot):
    """Test setting the transition duration"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    line_edit.setTransitionDuration(1000)

    assert line_edit.getTransitionDuration() == 1000

def test_set_easing_curve(qtbot):
    """Test setting the easing curve"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    easing_curve = QEasingCurve.Type.Linear
    line_edit.setEasingCurve(easing_curve)

    assert line_edit.getEasingCurve() == easing_curve

def test_set_hovered_color(qtbot):
    """Test setting the hovered text color"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    color = QColor(255, 0, 0)
    line_edit.setHoveredColor(color)

    assert line_edit.getHoveredColor() == color

def test_set_hovered_background_color(qtbot):
    """Test setting the hovered background color"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    color = QColor(255, 0, 0)
    line_edit.setHoveredBackgroundColor(color)

    assert line_edit.getHoveredBackgroundColor() == color

def test_set_hovered_border_color(qtbot):
    """Test setting the hovered border color"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    color = QColor(255, 0, 0)
    line_edit.setHoveredBorderColor(color)

    assert line_edit.getHoveredBorderColor() == color

def test_set_hovered_border_width(qtbot):
    """Test setting the hovered border width"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    line_edit.setHoveredBorderWidth(10)

    assert line_edit.getHoveredBorderWidth() == 10

def test_set_focused_color(qtbot):
    """Test setting the focused text color"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    color = QColor(255, 0, 0)
    line_edit.setFocusedColor(color)

    assert line_edit.getFocusedColor() == color

def test_set_focused_background_color(qtbot):
    """Test setting the focused background color"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    color = QColor(255, 0, 0)
    line_edit.setFocusedBackgroundColor(color)

    assert line_edit.getFocusedBackgroundColor() == color

def test_set_focused_border_color(qtbot):
    """Test setting the focused border color"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    color = QColor(255, 0, 0)
    line_edit.setFocusedBorderColor(color)

    assert line_edit.getFocusedBorderColor() == color

def test_set_focused_border_width(qtbot):
    """Test setting the focused border width"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    line_edit.setFocusedBorderWidth(10)

    assert line_edit.getFocusedBorderWidth() == 10

def test_set_disabled_color(qtbot):
    """Test setting the disabled text color"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    color = QColor(255, 0, 0)
    line_edit.setDisabledColor(color)

    assert line_edit.getDisabledColor() == color

def test_set_disabled_background_color(qtbot):
    """Test setting the disabled background color"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    color = QColor(255, 0, 0)
    line_edit.setDisabledBackgroundColor(color)

    assert line_edit.getDisabledBackgroundColor() == color

def test_set_disabled_border_color(qtbot):
    """Test setting the disabled border color"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    color = QColor(255, 0, 0)
    line_edit.setDisabledBorderColor(color)

    assert line_edit.getDisabledBorderColor() == color

def test_set_disabled_border_width(qtbot):
    """Test setting the disabled border width"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    line_edit.setDisabledBorderWidth(10)

    assert line_edit.getDisabledBorderWidth() == 10

def test_focus_in_out(qtbot):
    """Test focusing the widget"""

    line_edit = AnimatedLineEdit('Test')
    line_edit.setTransitionDuration(100)
    qtbot.addWidget(line_edit)

    # Simulate focus in event
    focus_event_in = QFocusEvent(QFocusEvent.Type.FocusIn)
    qt_api.QtWidgets.QApplication.instance().postEvent(line_edit, focus_event_in)

    # Wait for animation to complete
    QTest.qWait(250)

    # Placeholder text should be in the outside position
    assert line_edit.isPlaceholderInside() == False

    # Simulate focus out event
    focus_event_out = QFocusEvent(QFocusEvent.Type.FocusOut)
    qt_api.QtWidgets.QApplication.instance().postEvent(line_edit, focus_event_out)

    # Wait for animation to complete
    QTest.qWait(250)

    # Placeholder text should be in the inside position
    assert line_edit.isPlaceholderInside() == True

    # Simulate focus in event again
    focus_event_in = QFocusEvent(QFocusEvent.Type.FocusIn)
    qt_api.QtWidgets.QApplication.instance().postEvent(line_edit, focus_event_in)

    # Wait for animation to complete
    QTest.qWait(250)

    # Placeholder text should be in the outside position again
    assert line_edit.isPlaceholderInside() == False
