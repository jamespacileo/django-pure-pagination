import collections

from django.core.paginator import InvalidPage, EmptyPage, PageNotAnInteger
from django.conf import settings

from math import ceil
import functools

from django.template.loader import render_to_string

PAGINATION_SETTINGS = getattr(settings, "PAGINATION_SETTINGS", {})

PAGE_RANGE_DISPLAYED = PAGINATION_SETTINGS.get("PAGE_RANGE_DISPLAYED", 10)
MARGIN_PAGES_DISPLAYED = PAGINATION_SETTINGS.get("MARGIN_PAGES_DISPLAYED", 2)
SHOW_FIRST_PAGE_WHEN_INVALID = PAGINATION_SETTINGS.get("SHOW_FIRST_PAGE_WHEN_INVALID", False)


class Paginator(object):
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, request=None):
        self.object_list = object_list
        self.per_page = per_page
        self.orphans = orphans
        self.allow_empty_first_page = allow_empty_first_page
        self._num_pages = self._count = None
        self.request = request

    def validate_number(self, number):
        "Validates the given 1-based page number."
        try:
            number = int(number)
        except ValueError:
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            if SHOW_FIRST_PAGE_WHEN_INVALID:
                number = 1
            else:
                raise EmptyPage('That page number is less than 1')
        if number > self.num_pages:
            if number == 1 and self.allow_empty_first_page:
                pass
            elif SHOW_FIRST_PAGE_WHEN_INVALID:
                number = 1
            else:
                raise EmptyPage('That page contains no results')
        return number

    def page(self, number):
        "Returns a Page object for the given 1-based page number."
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return Page(self.object_list[bottom:top], number, self)

    def _get_count(self):
        "Returns the total number of objects, across all pages."
        if self._count is None:
            try:
                self._count = self.object_list.count()
            except (AttributeError, TypeError):
                # AttributeError if object_list has no count() method.
                # TypeError if object_list.count() requires arguments
                # (i.e. is of type list).
                self._count = len(self.object_list)
        return self._count
    count = property(_get_count)

    def _get_num_pages(self):
        "Returns the total number of pages."
        if self._num_pages is None:
            if self.count == 0 and not self.allow_empty_first_page:
                self._num_pages = 0
            else:
                hits = max(1, self.count - self.orphans)
                self._num_pages = int(ceil(hits / float(self.per_page)))
        return self._num_pages
    num_pages = property(_get_num_pages)

    def _get_page_range(self):
        """
        Returns a 1-based range of pages for iterating through within
        a template for loop.
        """
        return range(1, self.num_pages + 1)
    page_range = property(_get_page_range)

QuerySetPaginator = Paginator  # For backwards-compatibility.


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
        elif isinstance(result, collections.Iterable):
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


class Page(object):
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.paginator = paginator
        if paginator.request:
            # Reason: I just want to perform this operation once, and not once per page
            self.base_queryset = self.paginator.request.GET.copy()
            # self.base_queryset['page'] = 'page'
            # self.base_queryset = self.base_queryset.urlencode().replace('%', '%%').replace('page=page', 'page=%s')

        self.number = PageRepresentation(number, self._other_page_querystring(number))

    def __repr__(self):
        return '<Page %s of %s>' % (self.number, self.paginator.num_pages)

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    @add_page_querystring
    def next_page_number(self):
        return self.number + 1

    @add_page_querystring
    def previous_page_number(self):
        return self.number - 1

    def start_index(self):
        """
        Returns the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return (self.paginator.per_page * (self.number - 1)) + 1

    def end_index(self):
        """
        Returns the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page because there can be orphans.
        if self.number == self.paginator.num_pages:
            return self.paginator.count
        return self.number * self.paginator.per_page

    @add_page_querystring
    def pages(self):
        if self.paginator.num_pages <= PAGE_RANGE_DISPLAYED:
            return range(1, self.paginator.num_pages + 1)
        result = []
        left_side = PAGE_RANGE_DISPLAYED / 2
        right_side = PAGE_RANGE_DISPLAYED - left_side
        if self.number > self.paginator.num_pages - PAGE_RANGE_DISPLAYED / 2:
            right_side = self.paginator.num_pages - self.number
            left_side = PAGE_RANGE_DISPLAYED - right_side
        elif self.number < PAGE_RANGE_DISPLAYED / 2:
            left_side = self.number
            right_side = PAGE_RANGE_DISPLAYED - left_side
        for page in range(1, self.paginator.num_pages + 1):
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
            self.base_queryset['page'] = page_number
            return self.base_queryset.urlencode()

        # raise Warning("You must supply Paginator() with the request object for a proper querystring.")
        return 'page=%s' % page_number

    def render(self):
        return render_to_string('pure_pagination/pagination.html', {
            'current_page': self,
            'page_obj': self,  # Issue 9 https://github.com/jamespacileo/django-pure-pagination/issues/9
                               # Use same naming conventions as Django
        })
