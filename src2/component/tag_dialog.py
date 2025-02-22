from PySide6.QtWidgets import QLineEdit, QDialog, QFormLayout, QDialogButtonBox


class TagDialog(QDialog):
    def __init__(self, parent, title, current_tag=None):
        super().__init__(parent)
        self.setWindowTitle(title)

        self.tag_name = QLineEdit(self)
        self.tag_name.setText(current_tag if current_tag else "")

        layout = QFormLayout()
        layout.addRow("Tag Name:", self.tag_name)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def accept(self):
        if self.tag_name.text():
            super().accept()
        else:
            print("Tag name cannot be empty!")
