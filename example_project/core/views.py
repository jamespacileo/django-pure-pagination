# Create your views here.
from random import randint

from django.http import Http404
from django.shortcuts import render_to_response

from pure_pagination.paginator import Paginator
from pure_pagination.utils import paginated
from .names import names


def index(request):
    how_many_names = request.GET.get('how_many_names', 60)
    page_size = request.GET.get('page_size', 10)
    page_num = request.GET.get('page', 1)
    try:
        page_num = int(page_num)
        page_size = int(page_size)
        how_many_names = int(how_many_names)
    except ValueError:
        raise Http404

    selected_names = []
    total = len(names)
    for i in xrange(how_many_names):
        selected_names.append(names[randint(0, total - 1)])
    p = Paginator(selected_names, page_size, request=request)

    page = p.page(page_num)
    return render_to_response('index.html', {
        'page': page,
    })


def index2(request):
    how_many_names = request.GET.get('how_many_names', 60)
    page_size = request.GET.get('page_size', 10)
    try:
        how_many_names = int(how_many_names)
    except ValueError:
        raise Http404

    selected_names = []
    total = len(names)
    for i in xrange(how_many_names):
        selected_names.append(names[randint(0, total - 1)])

    # Using paginator to create pages
    page = paginated(request, selected_names, page_size)

    return render_to_response('index.html', {
        'page': page,
    })