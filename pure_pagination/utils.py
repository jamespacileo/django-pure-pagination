__author__ = 'allen'
from django.http.response import Http404
from django.conf import settings

from .paginator import Paginator


PAGINATION_SETTINGS = getattr(settings, "PAGINATION_SETTINGS", {})
PAGE_RANGE_DISPLAYED = PAGINATION_SETTINGS.get("PAGE_RANGE_DISPLAYED", 10)


def paginated(request, objects, page_size=PAGE_RANGE_DISPLAYED):
    """
    Returns a page of paginated objects
    """

    try:
        page_num = int(request.GET.get('page', '1'))
        page_size = int(page_size)
    except ValueError:
        raise Http404

    p = Paginator(objects, page_size, request=request)
    page = p.page(page_num)

    return page
