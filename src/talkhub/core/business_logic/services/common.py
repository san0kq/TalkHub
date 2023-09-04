from __future__ import annotations

import sys
import uuid
from io import BytesIO
from typing import TYPE_CHECKING

from PIL import Image

if TYPE_CHECKING:
    from django.core.files import File

from django.core.files.uploadedfile import InMemoryUploadedFile


def replace_file_name_to_uuid(file: File) -> File:
    """
    Replacing the uploaded file's name
    for users with a random UUID-based name.
    """
    file_extansion = file.name.split(".")[-1]
    file_name = str(uuid.uuid4())
    file.name = file_name + "." + file_extansion
    return file


def change_file_size(file: InMemoryUploadedFile) -> InMemoryUploadedFile:
    """
    Resizing an image to optimize storage.

    Returns a file stored in memory.
    """
    format = file.content_type.split("/")[-1].upper()
    output = BytesIO()
    with Image.open(file) as image:
        image.thumbnail(size=(200, 150))
        image.save(output, format=format, quality=100)

    return InMemoryUploadedFile(
        file=output,
        field_name=file.field_name,
        name=file.name,
        content_type=file.content_type,
        size=sys.getsizeof(output),
        charset=file.charset,
    )
