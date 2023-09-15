from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from django.http import HttpRequest
    from django.core.paginator import Page

from core.business_logic.exceptions import PageDoesNotExists
from django.core.paginator import EmptyPage, Paginator


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
