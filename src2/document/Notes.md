Example tag db JSON Structure:

{
  "all_tags": [
    "action",
    "comedy",
    "drama",
    "documentary",
    "thriller"
  ],
  "video_tags": {
    "path/to/video1.mp4": ["action", "thriller"],
    "path/to/video2.mp4": ["comedy", "drama"],
    "path/to/video3.mp4": ["documentary"]
  }
}

How to Use:

    Initialization: To initialize the database and set the path for the JSON file:

tag_db = TagDBHelper('tag_database.json')

Adding and Removing Tags:

    Add a new tag:

tag_db.add_tag('action')

Remove a tag:

    tag_db.remove_tag('comedy')

Adding/Removing Tags for a Video:

    Add tags for a specific video:

tag_db.add_video_tags('path/to/video1.mp4', ['action', 'drama'])

Remove tags for a specific video:

    tag_db.remove_video_tags('path/to/video1.mp4', ['action'])

Fetching Tags:

    Get tags for a specific video:

tags = tag_db.get_video_tags('path/to/video1.mp4')
print(tags)

Get all tags:

all_tags = tag_db.get_all_tags()
print(all_tags)