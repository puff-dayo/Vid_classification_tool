import json
import os


class TagDBHelper:
    def __init__(self, db_path, auto_save = False):
        self.db_path = db_path
        self.data = self.load_db()
        self.auto_save = auto_save

    def load_db(self):
        if not os.path.exists(self.db_path):
            self.initialize_db()
        with open(self.db_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def initialize_db(self):
        initial_data = {
            "all_tags": [],
            "video_tags": {}
        }
        self.save_db(initial_data)

    def save_db(self, data):
        with open(self.db_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def add_tag(self, tag):
        if tag not in self.data["all_tags"]:
            self.data["all_tags"].append(tag)
            if self.auto_save: self.save_db(self.data)
        else:
            print(f"Tag '{tag}' already exists in the database.")

    def remove_tag(self, tag):
        if tag in self.data["all_tags"]:
            # Remove tag from all_tags
            self.data["all_tags"].remove(tag)
            # Remove the tag from video_tags
            for video_path, tags in self.data["video_tags"].items():
                if tag in tags:
                    self.data["video_tags"][video_path].remove(tag)
            if self.auto_save: self.save_db(self.data)
        else:
            print(f"Tag '{tag}' not found in the database.")

    def add_video_tags(self, video_path, tags):
        if video_path not in self.data["video_tags"]:
            self.data["video_tags"][video_path] = tags
            if self.auto_save: self.save_db(self.data)
        else:
            self.data["video_tags"][video_path].extend(
                tag for tag in tags if tag not in self.data["video_tags"][video_path])
            if self.auto_save: self.save_db(self.data)

    def remove_video_tags(self, video_path, tags):
        if video_path in self.data["video_tags"]:
            self.data["video_tags"][video_path] = [tag for tag in self.data["video_tags"][video_path] if
                                                   tag not in tags]
            if self.auto_save: self.save_db(self.data)
        else:
            print(f"No tags found for video '{video_path}'.")

    def get_video_tags(self, video_path):
        normalized_path = os.path.normpath(video_path)
        return self.data["video_tags"].get(normalized_path, [])

    def get_all_tags(self):
        return self.data["all_tags"]

    def update_tag(self, current_tag, new_tag):
        self.remove_tag(current_tag)
        self.add_tag(new_tag)
        if self.auto_save: self.save_db(self.data)
