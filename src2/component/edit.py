import os
import platform

from PySide6.QtCore import QDir, QUrl, Signal, Slot, Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSplitter, QLabel, \
    QListWidget, QApplication, QFileSystemModel, QTreeView
from PySide6.QtGui import QIcon
import qtawesome as qta

from src2.component.menubar import create_menubar
from src2.helper.app_path_helper import load_dlls
from src2.helper.dark_theme import apply_dark

_ = load_dlls()
import mpv


class EditWindow(QMainWindow):
    directory_selected = Signal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("VCT - Edit")
        self.setGeometry(300, 300, 800, 600)

        self.icon_save = qta.icon('fa5s.save')

        self.init_ui()
        create_menubar(self)
        self.directory_selected.connect(self.update_navigation_panel)

        self.init_db()

    def init_ui(self):
        layout = QHBoxLayout()

        ##### Left Panel - File & Folder Navigator
        left_panel = QWidget()
        left_layout = QVBoxLayout()

        # Set up file system model
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath('')
        self.file_system_model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot)
        # Set up a QTreeView to display
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_system_model)
        self.tree_view.setRootIndex(self.file_system_model.index(''))
        self.tree_view.clicked.connect(self.on_file_selected)

        left_layout.addWidget(self.tree_view)
        left_panel.setLayout(left_layout)

        ##### Middle Panel - Video Playback & Info Display
        middle_panel = QWidget()
        middle_layout = QVBoxLayout()

        self.video_widget = QWidget(self)
        self.video_widget.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.video_widget.setAttribute(Qt.WA_NativeWindow)
        self.mpv_player = mpv.MPV(log_handler=print, loglevel='error', wid=str(int(self.video_widget.winId())))
        middle_layout.addWidget(self.video_widget)

        self.video_info_label = QLabel("Video Info: No video loaded.")
        middle_layout.addWidget(self.video_info_label)

        middle_panel.setLayout(middle_layout)

        ##### Right Panel - All Tags & Current Tags for Video
        right_panel = QWidget()
        right_layout = QVBoxLayout()

        self.all_tags_list = QListWidget()
        self.current_tags_list = QListWidget()

        # Add example tags to the all tags list (todo: should be loaded from the tag database)
        self.all_tags_list.addItems(["action", "comedy", "drama", "documentary", "thriller"])

        right_layout.addWidget(QLabel("All Tags"))
        right_layout.addWidget(self.all_tags_list)

        right_layout.addWidget(QLabel("Current Tags for Video"))
        right_layout.addWidget(self.current_tags_list)

        right_panel.setLayout(right_layout)

        # Save Button at the bottom
        button_save = QPushButton('Save')
        button_save.setIcon(self.icon_save)
        button_save.clicked.connect(self.save_changes)

        ###### Combine
        splitter = QSplitter()
        splitter.addWidget(left_panel)
        splitter.addWidget(middle_panel)
        splitter.addWidget(right_panel)

        layout.addWidget(splitter)

        # Adding Save button below the splitter (todo: replace by menu bar)
        layout.addWidget(button_save)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_video(self, video_path):
        video_path = os.path.normpath(video_path)
        if platform.system() == "Linux":
            self.mpv_player['vo'] = 'x11'
        else:
            self.mpv_player['vo'] = 'opengl'
        self.mpv_player['hwdec'] = 'auto'
        self.mpv_player.play(str(video_path))

        self.video_info_label.setText(f"Video Info: {video_path}")

    def save_changes(self):
        """Placeholder save function for handling tag saving or any other actions."""
        print("Changes saved!")

    def on_file_selected(self, index):
        selected_path = self.file_system_model.filePath(index)
        if selected_path.endswith(('.mp4', '.avi', '.mkv', '.mov')):
            print(f"loading {selected_path}")
            self.load_video(selected_path)

    @Slot(str)
    def update_navigation_panel(self, directory):
        self.file_system_model.setRootPath(directory)
        self.tree_view.setRootIndex(self.file_system_model.index(directory))

        # Truncate the directory path if it is too long
        max_length = 50
        if len(directory) > max_length:
            truncated_directory = directory[:max_length] + "..."
        else:
            truncated_directory = directory

        self.setWindowTitle(f"VCT Editing - {truncated_directory}")


if __name__ == '__main__':
    app = QApplication([])
    window = EditWindow()
    window.show()
    apply_dark(window)
    app.exec()
