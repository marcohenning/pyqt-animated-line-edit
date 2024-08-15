import sys
from PySide6.QtGui import QPalette
from PySide6.QtCore import QMargins
from PySide6.QtWidgets import QMainWindow, QApplication, QLineEdit
from src.pyqt_animated_line_edit import AnimatedLineEdit


class Window(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)

        # Window settings
        self.setWindowTitle('Example')
        self.setFixedSize(300, 165)

        # LineEdit 1
        self.username = AnimatedLineEdit('Username', self)
        self.username.setGeometry(90, 37, 120, 35)
        self.username.setBorderRadius(2)  # Set LineEdit border radius
        self.username.setPlaceholderFontSizeInner(10)  # Set placeholder font size for the inside position
        self.username.setPlaceholderFontSizeOuter(8)  # Set placeholder font size for the outside position
        self.username.setPadding(QMargins(12, 0, 12, 0))  # Set LineEdit padding
        self.username.setPlaceholderColorOutside(
            self.palette().color(QPalette.ColorRole.Highlight))  # Set placeholder color for the outside position

        # LineEdit 2
        self.password = AnimatedLineEdit('Password', self)
        self.password.setGeometry(90, 77, 120, 35)
        self.password.setBorderRadius(2)  # Set LineEdit border radius
        self.password.setPlaceholderFontSizeInner(10)  # Set placeholder font size for the inside position
        self.password.setPlaceholderFontSizeOuter(8)  # Set placeholder font size for the outside position
        self.password.setPadding(QMargins(12, 0, 12, 0))  # Set LineEdit padding
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderColorOutside(
            self.palette().color(QPalette.ColorRole.Highlight))  # Set placeholder color for the outside position


# Run the example
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
