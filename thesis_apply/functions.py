from django.core.files.storage import default_storage
from django.utils.crypto import get_random_string
import os

def handleUploadFile(file):
    # Get the file extension
    extension = os.path.splitext(file.name)[1]
    unique_filename = f"cv_{get_random_string(length=10)}{extension}"
    file_name = default_storage.save('cv/' + unique_filename, file)
    return default_storage.url(file_name)