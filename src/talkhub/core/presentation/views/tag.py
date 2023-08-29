from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

from core.business_logic.dto import SearchTagDTO, TrendingDTO
from core.business_logic.exceptions import PageDoesNotExists
from core.business_logic.services import find_tags, get_trending_tags, paginate_pages
from core.presentation.converters import convert_data_from_form_to_dto
from core.presentation.forms import SearchTagForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View


class TagsView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = SearchTagForm(request.GET)
        if form.is_valid():
            data = convert_data_from_form_to_dto(dto=SearchTagDTO, data_from_form=form.cleaned_data)
            tweets = find_tags(data=data)
            try:
                tweets_paginated, prev_page, next_page = paginate_pages(request, tweets, per_page=20)
            except PageDoesNotExists as err:
                return HttpResponseBadRequest(content=err)

            form = SearchTagForm()
            context = {
                "form": form,
                "tweets": tweets_paginated,
                "prev_page": prev_page,
                "next_page": next_page,
                "tag_name": data.name,
            }
            return render(request, "tag.html", context=context)
        else:
            return None


class TrendingView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest) -> HttpResponse:
        data = TrendingDTO(user=request.user)
        tags = get_trending_tags(data=data)
        context = {"tags": tags}
        return render(request, "trending.html", context=context)
