import os
import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QMessageBox

from src2.component.tag_dialog import ExitDialog


def save_db(window):
    window.to_save_database.emit("")


def create_menubar(window, config):
    menubar = window.menuBar()

    # File Menu
    file_menu = menubar.addMenu("File")

    open_directory_action = QAction("Open Directory", window)
    open_directory_action.triggered.connect(lambda: open_directory(window))
    file_menu.addAction(open_directory_action)

    auto_save_action = QAction("Auto Save", window)
    auto_save_action.setCheckable(True)
    auto_save_action.setChecked(True if config['main'].get('auto_save') == "True" else False)
    auto_save_action.triggered.connect(lambda: toggle_auto_save(auto_save_action, window, config))
    file_menu.addAction(auto_save_action)

    save_action = QAction("Save Database", window)
    save_action.triggered.connect(lambda: save_db(window))
    file_menu.addAction(save_action)

    return_launcher_action = QAction("Exit edit", window)
    return_launcher_action.triggered.connect(lambda: return_to_launcher(window))
    file_menu.addAction(return_launcher_action)

    # Tool Menu
    tool_menu = menubar.addMenu("Tool")
    restore = QAction("Auto reconnect video file", window)
    """todo: add"""
    tool_menu.addAction(restore)

    # Info Menu
    info_menu = menubar.addMenu("Info")

    help_action = QAction("Help", window)
    help_action.triggered.connect(show_help)
    info_menu.addAction(help_action)

    about_action = QAction("About", window)
    about_action.triggered.connect(show_about)
    info_menu.addAction(about_action)


def open_directory(window):
    directory = QFileDialog.getExistingDirectory(None, "Select Directory", os.path.expanduser("~"))
    if directory:
        print(f"Selected Directory: {directory}")

        window.directory_selected.emit(directory)


def return_to_launcher(window):
    exit_dialog = ExitDialog(window, window)
    exit_dialog.exec()


def show_help():
    QMessageBox.information(None, "Help", "This is the Help section. There is no help.")


def show_about():
    QMessageBox.information(None, "About", "Placeholderrrrrrrr")

def toggle_auto_save(action, window, config):
    if action.isChecked():
        window.db_helper.auto_save = True
        config['main']['auto_save'] = True
    else:
        window.db_helper.auto_save = False
        config['main']['auto_save'] = False