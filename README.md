# PyQt Animated LineEdit

shields

short description

gif

## About

long description

## Installation

```
pip install ...
```

## Example

```python
from PyQt6.QtGui import QPalette
from PyQt6.QtCore import QMargins
from PyQt6.QtWidgets import QMainWindow
from pyqt_animated_line_edit import AnimatedLineEdit


class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        # Window settings
        self.setWindowTitle('Example')
        self.setFixedSize(300, 165)

        # AnimatedLineEdit
        self.username = AnimatedLineEdit('Username', self)
        self.username.setGeometry(90, 37, 120, 35)
        self.username.setBorderRadius(2)
        self.username.setPlaceholderFontSizeInner(10)
        self.username.setPlaceholderFontSizeOuter(8)
        self.username.setPadding(QMargins(12, 0, 12, 0))
        self.username.setPlaceholderColorOutside(
            self.palette().color(QPalette.ColorRole.Highlight))
```

## Documentation

| Method                                                  | Description                                                  |
|---------------------------------------------------------|--------------------------------------------------------------|
| `setPlaceholderText(self, text: str)`                   | Set the placeholder text                                     |
| `setColor(self, color: QColor)`                         | Set the text color                                           |
| `setPlaceholderColor(self, color: QColor)`              | Set the placeholder text color                               |
| `setPlaceholderColorOutside(self, color: QColor)`       | Set the placeholder text color for the outside position      |
| `setBackgroundColor(self, color: QColor)`               | Set the background color                                     |
| `setBorderColor(self, color: QColor)`                   | Set the border color                                         |
| `setBorderWidth(self, width: int)`                      | Set the border width                                         |
| `setBorderRadius(self, radius: int)`                    | Set the border radius                                        |
| `setPlaceholderFontFamily(self, family: str)`           | Set the placeholder text font family                         |
| `setPlaceholderFontSizeInner(self, size: int)`          | Set the placeholder text font size for the inside position   |
| `setPlaceholderFontSizeOuter(self, size: int)`          | Set the placeholder text font size for the outside position  |
| `setPlaceholderFontBold(self, enable: bool)`            | Set the placeholder text bold                                |
| `setPlaceholderFontItalic(self, enable: bool)`          | Set the placeholder text italic                              |
| `setPadding(self, padding: QMargins)`                   | Set the padding                                              |
| `setTransitionDuration(self, duration: int)`            | Set the duration of the placeholder transition animation     |
| `setEasingCurve(self, easing_curve: QEasingCurve.Type)` | Set the easing curve of the placeholder transition animation |
| `setHoveredColor(self, color: QColor)`                  | Set the hovered text color                                   |
| `setHoveredBackgroundColor(self, color: QColor)`        | Set the hovered background color                             |
| `setHoveredBorderColor(self, color: QColor)`            | Set the hovered border color                                 |
| `setHoveredBorderWidth(self, width: int)`               | Set the hovered border width                                 |
| `setFocusedColor(self, color: QColor)`                  | Set the focused text color                                   |
| `setFocusedBackgroundColor(self, color: QColor)`        | Set the focused background color                             |
| `setFocusedBorderColor(self, color: QColor)`            | Set the focused border color                                 |
| `setFocusedBorderWidth(self, width: int)`               | Set the focused border width                                 |
| `setDisabledColor(self, color: QColor)`                 | Set the disabled text color                                  |
| `setDisabledBackgroundColor(self, color: QColor)`       | Set the disabled background color                            |
| `setDisabledBorderColor(self, color: QColor)`           | Set the disabled border color                                |
| `setDisabledBorderWidth(self, width: int)`              | Set the disabled border width                                |

## License

License
