import os.path
import sys

import qdarktheme
import qtawesome as qta
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QPushButton,
                               QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout)

from src2.component.edit import EditWindow
from src2.helper.app_path_helper import RES_PATH
from src2.helper.config_helper import load_config
from src2.helper.dark_theme import apply_dark


class VidTagLaunch(QMainWindow):
    def __init__(self, config):
        super().__init__()

        self.setWindowTitle("VCT")

        self.init_icons()
        self.init_ui()

    def init_icons(self):
        self.icon_home = qta.icon('fa5s.home')
        self.icon_edit = qta.icon('fa5s.edit')
        self.icon_preferences = qta.icon('fa5s.cogs')
        self.icon_about = qta.icon('fa5s.info-circle')

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)

        button_view = QPushButton(' View only')
        button_view.setIcon(self.icon_home)

        button_edit_view = QPushButton(' Edit + View')
        button_edit_view.clicked.connect(self.open_edit_window)
        button_edit_view.setIcon(self.icon_edit)

        button_preferences = QPushButton(' Preferences')
        button_preferences.setIcon(self.icon_preferences)

        button_about = QPushButton(' About')
        button_about.setIcon(self.icon_about)

        info_L = QHBoxLayout()
        info_L.addStretch()
        info_L.addWidget(QLabel("Version: dev 9"))
        info_W = QWidget()
        info_W.setLayout(info_L)

        layout.addWidget(button_view)
        layout.addWidget(button_edit_view)
        layout.addWidget(button_preferences)
        layout.addWidget(button_about)
        layout.addWidget(info_W)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def open_edit_window(self):
        self.edit_window = EditWindow(config)
        self.edit_window.show()
        apply_dark(self.edit_window)


if __name__ == '__main__':
    config = load_config()

    os.environ["LANG"] = "en_US.UTF-8"

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(RES_PATH, 'main_icon.png')))
    qdarktheme.setup_theme("auto")

    gui = VidTagLaunch(config)
    gui.show()
    apply_dark(gui)

    sys.exit(app.exec())
