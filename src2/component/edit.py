import os
import platform

from PySide6.QtCore import QDir, Signal, Slot, Qt
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QSplitter, QLabel, \
    QListWidget, QApplication, QFileSystemModel, QTreeView, QPushButton, QMenu, QSizePolicy
from PySide6.QtGui import QIcon, QAction
import qtawesome as qta

from src2.component.menubar import create_menubar
from src2.component.tag_dialog import TagDialog
from src2.helper.app_path_helper import load_dlls
from src2.helper.config_helper import load_config
from src2.helper.dark_theme import apply_dark
from src2.helper.tag_db_helper import TagDBHelper

_ = load_dlls()
import mpv


class EditWindow(QMainWindow):
    directory_selected = Signal(str)
    to_save_database = Signal(str)

    def __init__(self, config):
        super().__init__()

        self.setWindowTitle("VCT - Edit")
        self.resize(1280, 600)

        self.icon_save = qta.icon('fa5s.save')

        self.init_ui()
        create_menubar(self)

        self.directory_selected.connect(self.update_navigation_panel)
        self.to_save_database.connect(self.save_changes)

        self.db_path = config['main'].get('db_file')
        print(self.db_path)
        self.init_db()

    def init_db(self):
        self.db_helper = TagDBHelper(self.db_path)
        self.all_tags_list.clear()
        all_tags = self.db_helper.get_all_tags()
        self.all_tags_list.addItems(all_tags)

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

        self.add_tag_button = QPushButton("Add")
        self.add_tag_button.clicked.connect(self.add_new_tag)

        self.all_tags_list = QListWidget()
        self.all_tags_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.all_tags_list.customContextMenuRequested.connect(self.show_context_menu)

        self.current_tags_list = QListWidget()

        all_tag_L = QHBoxLayout()
        all_tag_L.setContentsMargins(0, 0, 0, 0)
        all_tag_L.setSpacing(0)
        all_tag_W = QWidget()
        all_tag_L.addWidget(QLabel("All Tags"))
        all_tag_L.addStretch()
        all_tag_L.addWidget(self.add_tag_button)
        all_tag_W.setLayout(all_tag_L)

        right_layout.addWidget(all_tag_W)
        right_layout.addWidget(self.all_tags_list)

        right_layout.addWidget(QLabel("Current Tags for Video"))
        right_layout.addWidget(self.current_tags_list)

        right_panel.setLayout(right_layout)

        ###### Combine
        splitter = QSplitter()
        splitter.addWidget(left_panel)
        splitter.addWidget(middle_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 10)
        splitter.setStretchFactor(1, 25)
        splitter.setStretchFactor(2, 5)

        layout.addWidget(splitter)

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
        self.db_helper.save_db(self.db_helper.data)
        """todo: auto save?"""
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

    def show_context_menu(self, pos):
        context_menu = QMenu(self)

        selected_item = self.all_tags_list.itemAt(pos)
        if selected_item:
            modify_action = QAction("Modify", self)
            modify_action.triggered.connect(lambda: self.modify_tag(selected_item))
            context_menu.addAction(modify_action)

            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self.delete_tag(selected_item))
            context_menu.addAction(delete_action)

        context_menu.exec(self.all_tags_list.mapToGlobal(pos))

    def modify_tag(self, tag_item):
        current_tag = tag_item.text()
        dialog = TagDialog(self, "Modify Tag", current_tag)
        if dialog.exec():
            new_tag = dialog.tag_name.text()
            tag_item.setText(new_tag)
            self.db_helper.update_tag(current_tag, new_tag)

    def delete_tag(self, tag_item):
        tag_name = tag_item.text()
        self.db_helper.remove_tag(tag_name)
        self.all_tags_list.takeItem(self.all_tags_list.row(tag_item))

    def add_new_tag(self):
        dialog = TagDialog(self, "Add New Tag")
        if dialog.exec():
            new_tag = dialog.tag_name.text()
            self.all_tags_list.addItem(new_tag)
            self.db_helper.add_tag(new_tag)


if __name__ == '__main__':
    app = QApplication([])
    window = EditWindow(load_config())
    window.show()
    apply_dark(window)
    app.exec()
