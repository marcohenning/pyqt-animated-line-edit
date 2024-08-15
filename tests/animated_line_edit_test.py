from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import QEasingCurve, QMargins
from src.pyqt_animated_line_edit.animated_line_edit import AnimatedLineEdit


def test_initial_values(qtbot):
    """Test initial values after instantiating"""

    line_edit = AnimatedLineEdit('Test')
    qtbot.addWidget(line_edit)

    assert line_edit.getPlaceholderText() == 'Test'
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
