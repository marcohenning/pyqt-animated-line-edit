# PyQt Animated LineEdit

[![PyPI](https://img.shields.io/badge/pypi-v1.0.0-blue)](https://pypi.org/project/pyqt-animated-line-edit)
[![Python](https://img.shields.io/badge/python-3.7+-blue)](https://github.com/marcohenning/pyqt-animated-line-edit)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/marcohenning/pyqt-animated-line-edit/blob/master/LICENSE)
[![Coverage](https://img.shields.io/badge/coverage-96%25-neon)](https://github.com/marcohenning/pyqt-animated-line-edit)
[![Build](https://img.shields.io/badge/build-passing-neon)](https://github.com/marcohenning/pyqt-animated-line-edit)

A modern and animated version of the QLineEdit widget for PyQt and PySide.

![Main](https://github.com/user-attachments/assets/267832aa-44a3-4532-aca9-7e3b393e8a4b)

## About

The widget is based on Qt's QLineEdit widget and improves it by animating the placeholder text between two positions. If the widget is not in focus and does not contain any text, the placeholder will be in the normal (inside) position. When the widget is focused, however, the placeholder text moves to the top of the widget (outside position), creating a gap in the border. If the widget loses focus and does not contain any text, the placeholder moves to the normal position again. If the widget contains text, the placeholder will stay in position. This way the placeholder is always visible. The widget is highly customizable with options such as changing the duration and easing curve of the animation and changing the font and color for both placeholder positions independently.

## Installation

```
pip install pyqt-animated-line-edit
```

## Example

```python
from PyQt6.QtCore import QMargins
from PyQt6.QtWidgets import QMainWindow
from pyqt_animated_line_edit import AnimatedLineEdit


class Window(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)

        # AnimatedLineEdit
        self.username = AnimatedLineEdit('Username', self)
        self.username.setBorderRadius(2)
        self.username.setPlaceholderFontSizeInner(10)
        self.username.setPlaceholderFontSizeOuter(8)
        self.username.setPadding(QMargins(12, 0, 12, 0))
```

## Documentation

> **IMPORTANT:** <br>Styling of the widget must not be done by setting the stylesheet manually as the widget calculates the stylesheet itself and overrides it. Use the provided methods such as `setBackgroundColor()`, `setHoveredBackgroundColor()`, `setFocusedBackgroundColor()` and `setDisabledBackgroundColor()` instead.

| Method                                                  | Description                                                                                                 |
|---------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| `setPlaceholderText(self, text: str)`                   | Set the text displayed as placeholder                                                                       |
| `setTransitionDuration(self, duration: int)`            | Set the duration of the placeholder transition animation                                                    |
| `setEasingCurve(self, easing_curve: QEasingCurve.Type)` | Set the easing curve of the placeholder transition animation                                                |
| `setPlaceholderColor(self, color: QColor)`              | Set the color of the placeholder text (for both positions if the color for the outside position is not set) |
| `setPlaceholderColorOutside(self, color: QColor)`       | Set the color of the placeholder text for the outside position                                              |
| `setPlaceholderFontFamily(self, family: str)`           | Set the font family of the placeholder text (both positions)                                                |
| `setPlaceholderFontSizeInner(self, size: int)`          | Set the font size of the placeholder text for the inside position                                           |
| `setPlaceholderFontSizeOuter(self, size: int)`          | Set the font size of the placeholder text for the outside position                                          |
| `setPlaceholderFontBold(self, enable: bool)`            | Set the weight of the placeholder text to be bold or regular                                                |
| `setPlaceholderFontItalic(self, enable: bool)`          | Set the placeholder text to be italic or regular                                                            |
| `setColor(self, color: QColor)`                         | Set the regular color of the text                                                                           |
| `setBackgroundColor(self, color: QColor)`               | Set the regular color of the background                                                                     |
| `setBorderColor(self, color: QColor)`                   | Set the regular color of the border                                                                         |
| `setBorderWidth(self, width: int)`                      | Set the regular width of the border                                                                         |
| `setBorderRadius(self, radius: int)`                    | Set the radius of the border                                                                                |
| `setPadding(self, padding: QMargins)`                   | Set the padding of the widget                                                                               |
| `setHoveredColor(self, color: QColor)`                  | Set the text color for when the widget is hovered over                                                      |
| `setHoveredBackgroundColor(self, color: QColor)`        | Set the background color for when the widget is hovered over                                                |
| `setHoveredBorderColor(self, color: QColor)`            | Set the border color for when the widget is hovered over                                                    |
| `setHoveredBorderWidth(self, width: int)`               | Set the border width for when the widget is hovered over                                                    |
| `setFocusedColor(self, color: QColor)`                  | Set the text color for when the widget is focused                                                           |
| `setFocusedBackgroundColor(self, color: QColor)`        | Set the background color for when the widget is focused                                                     |
| `setFocusedBorderColor(self, color: QColor)`            | Set the border color for when the widget is focused                                                         |
| `setFocusedBorderWidth(self, width: int)`               | Set the border width for when the widget is focused                                                         |
| `setDisabledColor(self, color: QColor)`                 | Set the text color for when the widget is disabled                                                          |
| `setDisabledBackgroundColor(self, color: QColor)`       | Set the background color for when the widget is disabled                                                    |
| `setDisabledBorderColor(self, color: QColor)`           | Set the border color for when the widget is disabled                                                        |
| `setDisabledBorderWidth(self, width: int)`              | Set the border width for when the widget is disabled                                                        |

## License

This software is licensed under the [MIT license](https://github.com/marcohenning/pyqt-animated-line-edit/blob/master/LICENSE).
