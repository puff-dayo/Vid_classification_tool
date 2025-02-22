import ctypes as ct
import os.path
import platform
import sys

import darkdetect
import qdarktheme
import qtawesome as qta
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QPushButton,
                               QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout)

from src2.component.edit import EditWindow
from src2.helper.app_path_helper import RES_PATH
from src2.helper.config_helper import load_config


def dark_title_bar(hwnd, use_dark_mode=False):
    if platform.system() != "Windows":
        print("Dark mode is only supported on Windows.")
        return

    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 1 if use_dark_mode else 0
    value = ct.c_int(value)
    result = set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))
    if result != 0:
        print(f"Failed to set dark mode: {result}")


class VidTagLaunch(QMainWindow):
    def __init__(self, config):
        super().__init__()

        self.setWindowTitle("VCT")

        self.log_file = config['main'].get('log_file', 'log.txt')

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
        info_L.addWidget(QLabel("Version: dev 1"))
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

    def refresh_window(self, dx=1, dy=1):
        current_geometry = self.geometry()
        new_width = current_geometry.width() + dx
        new_height = current_geometry.height() + dy
        self.setGeometry(current_geometry.x(), current_geometry.y(), new_width, new_height)
        self.setGeometry(current_geometry.x(), current_geometry.y(), current_geometry.width(),
                         current_geometry.height())

    def open_edit_window(self):
        self.edit_window = EditWindow()
        self.edit_window.show()

        winId = self.edit_window.winId()
        dark_title_bar(winId, use_dark_mode=darkdetect.isDark())
        self.edit_window.refresh_window()

if __name__ == '__main__':
    config = load_config()

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(RES_PATH, 'main_icon.png')))
    qdarktheme.setup_theme("auto")

    gui = VidTagLaunch(config)
    gui.show()

    winId = gui.winId()
    dark_title_bar(winId, use_dark_mode=darkdetect.isDark())
    gui.refresh_window()

    sys.exit(app.exec())
