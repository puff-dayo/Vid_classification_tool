from PySide6.QtWidgets import QLineEdit, QDialog, QFormLayout, QDialogButtonBox, QLabel, QPushButton, QTextEdit

from src2.helper.dark_theme import apply_dark


class TagDialog(QDialog):
    def __init__(self, parent, title, current_tag=None):
        super().__init__(parent)
        self.setWindowTitle(title)

        self.tag_name = QTextEdit(self)
        self.tag_name.setText(current_tag if current_tag else "")

        layout = QFormLayout()
        layout.addRow("Tag Name:", self.tag_name)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)

        apply_dark(self)

    def accept(self):
        if self.tag_name.toPlainText():
            super().accept()
        else:
            print("Tag name cannot be empty!")


class WarnDialog(QDialog):
    def __init__(self, parent, current_tag=None):
        super().__init__(parent)
        self.setWindowTitle("CONFIRM REMOVE")

        self.tag_name = QLineEdit(self)
        self.tag_name.setDisabled(True)
        self.tag_name.setText(current_tag if current_tag else "")

        layout = QFormLayout()
        layout.addRow("Tag Name:", self.tag_name)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)

        apply_dark(self)

    def accept(self):
        super().accept()


class ExitDialog(QDialog):
    def __init__(self, parent, window):
        super().__init__(parent)
        self.setWindowTitle("CONFIRM EXIT")

        layout = QFormLayout()
        layout.addRow(QLabel("Save before exit?"))

        self.save_and_quit_button = QPushButton("Save and Quit")
        self.dont_save_and_quit_button = QPushButton("Quit not save")
        self.dont_quit_button = QPushButton("Don't Quit")

        self.save_and_quit_button.clicked.connect(self.save_and_quit)
        self.dont_save_and_quit_button.clicked.connect(self.dont_save_and_quit)
        self.dont_quit_button.clicked.connect(self.dont_quit)

        layout.addWidget(self.save_and_quit_button)
        layout.addWidget(self.dont_save_and_quit_button)
        layout.addWidget(self.dont_quit_button)

        self.setLayout(layout)

        apply_dark(self)

        self.window = window

    def save_and_quit(self):
        print("Saving and quitting...")
        self.window.to_save_database.emit("quit")
        self.accept()  # Close the dialog

    def dont_save_and_quit(self):
        print("Not saving and quitting...")
        self.window.on_save_completed_and_quit()
        self.accept()  # Close the dialog

    def dont_quit(self):
        print("Not quitting...")
        self.reject()