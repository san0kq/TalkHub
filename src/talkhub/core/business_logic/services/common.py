from __future__ import annotations

import sys
import uuid
from io import BytesIO
from typing import TYPE_CHECKING, Iterable

from PIL import Image

if TYPE_CHECKING:
    from django.http import HttpRequest
    from django.core.paginator import Page

from core.business_logic.exceptions import PageDoesNotExists
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.paginator import EmptyPage, Paginator

if TYPE_CHECKING:
    from django.core.files import File


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


def paginate_pages(request: HttpRequest, data: Iterable, per_page: int) -> tuple[Page, int, int]:
    """
    Function used for pagination in controllers.
    It takes a request object to retrieve the page number if provided;
    if not, it defaults to the first page.
    It also takes data (an iterable object) and the maximum number of data objects per page.
    """
    try:
        page_number = request.GET["page"]
    except KeyError:
        page_number = 1

    paginator = Paginator(data, per_page)

    try:
        data_paginated = paginator.page(page_number)

    except EmptyPage:
        raise PageDoesNotExists("Page with provided number doesn't exist.")

    if data_paginated.has_next():
        next_page = data_paginated.next_page_number()
    else:
        next_page = None

    if data_paginated.has_previous():
        prev_page = data_paginated.previous_page_number()
    else:
        prev_page = None

    return data_paginated, prev_page, next_page
