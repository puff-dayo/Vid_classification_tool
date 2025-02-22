import os

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QMessageBox


def save_db(window):
    window.to_save_database.emit("")


def create_menubar(window):
    menubar = window.menuBar()

    # File Menu
    file_menu = menubar.addMenu("File")

    open_directory_action = QAction("Open Directory", window)
    open_directory_action.triggered.connect(lambda: open_directory(window))
    file_menu.addAction(open_directory_action)

    save_action = QAction("Save Database", window)
    save_action.triggered.connect(lambda: save_db(window))
    file_menu.addAction(save_action)

    return_launcher_action = QAction("Return to Launcher", window)
    return_launcher_action.triggered.connect(return_to_launcher)
    file_menu.addAction(return_launcher_action)

    exit_action = QAction("Exit App", window)
    exit_action.triggered.connect(window.close)
    file_menu.addAction(exit_action)

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


def return_to_launcher():
    print("Returning to Launcher...")


def show_help():
    QMessageBox.information(None, "Help", "This is the Help section. There is no help.")


def show_about():
    QMessageBox.information(None, "About", "Placeholderrrrrrrr")
