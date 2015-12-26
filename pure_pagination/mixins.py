from pure_pagination.paginator import Paginator


class PaginationMixin(object):
    """
    Mixin for generic class-based views (e.g. django.views.generic.ListView)
    """
    # Replace the default django.core paginator by pure_pagination.Paginator
    paginator_class = Paginator

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        # Pass the request object to the paginator to keep the parameters in the url querystring ("?page=2&old_param=...")
        request = self.request
        return self.paginator_class(queryset, per_page, orphans=orphans, allow_empty_first_page=allow_empty_first_page, request=request)
