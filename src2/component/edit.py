from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon
import qtawesome as qta

class EditWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Edit Window")
        self.setGeometry(300, 300, 400, 300)

        self.icon_save = qta.icon('fa5s.save')

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        button_save = QPushButton('Save')
        button_save.setIcon(self.icon_save)

        layout.addWidget(button_save)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def refresh_window(self, dx=1, dy=1):
        current_geometry = self.geometry()
        new_width = current_geometry.width() + dx
        new_height = current_geometry.height() + dy
        self.setGeometry(current_geometry.x(), current_geometry.y(), new_width, new_height)
        self.setGeometry(current_geometry.x(), current_geometry.y(), current_geometry.width(),
                         current_geometry.height())

