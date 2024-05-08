from django.db import models
from django.contrib.auth.models import User
from pathlib import Path
from datetime import datetime
import os


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "e",
    "j",
    "z",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "y",
    "",
    "e",
    "yu",
    "u",
    "ja",
    "je",
    "ji",
    "g",
)

image_files = {".jpeg", ".png", ".jpg", ".svg", ".bmp", ".ico", ".gif"}
video_files = {".mp4", ".mov", ".webm", ".avi", "mkv", ".wmv", ".flv"}
audio_files = {".mp3", ".wav", ".m4a", ".aiff", ".ogg", ".cda"}
document_files = {
    ".docx",
    ".doc",
    ".pptx",
    ".xlsx",
    ".html",
    ".htm",
    ".html5",
    ".txt",
    ".ini",
    ".xml",
    ".ppt",
    ".py",
    ".md",
    ".toml",
    "yml",
    ".cpp",
    ".h",
    ".java",
    ".css",
    ".js",
    ".csv",
}
archive_files = {".rar", ".rar4", ".zip", ".tar", ".bz2", ".7z", ".apk", ".dmg", ".jar"}
other_files = {}


FILE_TYPES = {
    "image": image_files,
    "video": video_files,
    "audio": audio_files,
    "document": document_files,
    "archive": archive_files,
    "other": other_files,
}


def get_file_type(filename):
    """
    Determines the file type of file based on its extension.

    Args:
    filename (str): The name of the file.

    Returns:
    str: The determined file type, or 'other' if the file type cannot be determined.
    """
    extension = Path(filename).suffix
    TRANS = {}
    for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(cyrillic)] = latin
        TRANS[ord(cyrillic.lower())] = latin.lower()

    for file_type, extensions in FILE_TYPES.items():
        if extension in extensions:
            return file_type
    return "other"


def update_filename(instance, filename):
    """
    Generates a new filename using the current date and time to ensure uniqueness and sorts it into a folder based on its type.

    Args:
    instance: The instance of the model where the file is being attached.
    filename (str): The original file name uploaded by the user.

    Returns:
    str: A new file path including the folder and new filename.
    """
    filepath = Path(filename)
    now = datetime.now().strftime("%Y%m%d-%H%M")
    filename = f"{now}_{filepath.name}"
    type_id = get_file_type(filepath.name)
    return os.path.join(type_id, filename)


class UserFile(models.Model):
    """
    Model representing a user's file including metadata about the file.

    Attributes:
    filepath (FileField): Path to the file including the filename.
    file_description (CharField): Optional description of the file.
    uploaded_at (DateTimeField): The datetime when the file was uploaded, set automatically.
    user (ForeignKey): Reference to the User who owns the file.
    filename (CharField): The name of the file.
    file_type (CharField): The type of file, determined automatically by the system.
    """

    filepath = models.FileField()
    file_description = models.CharField(max_length=255, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, related_name="files", on_delete=models.CASCADE, null=True
    )
    filename = models.CharField(max_length=255, null=True)
    file_type = models.CharField("File type", max_length=50, default="other")

    def save(self, **kwargs):
        """
        Overwrites the save method to ensure the filename and file type are set when the file is saved.
        """
        self.filename = self.filepath.name
        self.file_type = get_file_type(self.filepath.name)
        super().save(**kwargs)
