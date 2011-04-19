from django.conf import settings
from django.core.paginator import Paginator as CorePaginator, Page as CorePage, InvalidPage, PageNotAnInteger, EmptyPage
from math import ceil
import functools

from django.template.loader import render_to_string

PAGINATION_SETTINGS = getattr(settings, "PAGINATION_SETTINGS", {})

PAGE_RANGE_DISPLAYED = PAGINATION_SETTINGS.get("PAGE_RANGE_DISPLAYED", 10)
MARGIN_PAGES_DISPLAYED = PAGINATION_SETTINGS.get("MARGIN_PAGES_DISPLAYED", 2)


class Paginator(CorePaginator):
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, request=None):
        super(Paginator, self).__init__(object_list, per_page, orphans=orphans, allow_empty_first_page=allow_empty_first_page)
        self.request = request

QuerySetPaginator = Paginator # For backwards-compatibility.

class PageRepresentation(int):
    def __new__(cls, x, querystring):
        obj = int.__new__(cls, x)
        obj.querystring = querystring
        return obj


def add_page_querystring(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if isinstance(result, int):
            querystring = self._other_page_querystring(result)
            return PageRepresentation(result, querystring)
        elif isinstance(result, list):
            new_result = []
            for number in result:
                if isinstance(number, int):
                    querystring = self._other_page_querystring(number)
                    new_result.append(PageRepresentation(number, querystring))
                else:
                    new_result.append(number)
            return new_result
        return result
        
    return wrapper

class Page(CorePage):
    def __init__(self, object_list, number, paginator):
        super(Page, self).__init__(object_list, number, paginator)        
        if paginator.request:
            # Reason: I just want to perform this operation once, and not once per page
            self.base_queryset = self.paginator.request.GET.copy()
            self.base_queryset['page'] = 'page'
            self.base_queryset = self.base_queryset.urlencode().replace('page=page', 'page=%s')
            
        self.number = PageRepresentation(number, self._other_page_querystring(number))

    def __repr__(self):
        return '<Page %s of %s>' % (self.number, self.paginator.num_pages)


    @add_page_querystring
    def next_page_number(self):
        return self.number + 1

    @add_page_querystring
    def previous_page_number(self):
        return self.number - 1

    
    @add_page_querystring
    def pages(self):
        if self.paginator.num_pages <= PAGE_RANGE_DISPLAYED:
            return range(1, self.paginator.num_pages+1)
        result = []
        left_side = PAGE_RANGE_DISPLAYED/2
        right_side = PAGE_RANGE_DISPLAYED - left_side
        if self.number > self.paginator.num_pages - PAGE_RANGE_DISPLAYED/2:
            right_side = self.paginator.num_pages - self.number
            left_side = PAGE_RANGE_DISPLAYED - right_side
        elif self.number < PAGE_RANGE_DISPLAYED/2:
            left_side = self.number
            right_side = PAGE_RANGE_DISPLAYED - left_side
        for page in xrange(1, self.paginator.num_pages+1):
            if page <= MARGIN_PAGES_DISPLAYED:
                result.append(page)
                continue
            if page > self.paginator.num_pages - MARGIN_PAGES_DISPLAYED:
                result.append(page)
                continue
            if (page >= self.number - left_side) and (page <= self.number + right_side):
                result.append(page)
                continue
            if result[-1]:
                result.append(None)

        return result

    def _other_page_querystring(self, page_number):
        """
        Returns a query string for the given page, preserving any
        GET parameters present.
        """
        if self.paginator.request:
            return self.base_queryset %page_number

        #raise Warning("You must supply Paginator() with the request object for a proper querystring.")
        return 'page=%s' %page_number

    def render(self):
        return render_to_string('pure_pagination/pagination.html', {'current_page':self})
        
