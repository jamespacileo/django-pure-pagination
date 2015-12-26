======================
django-pure-pagination
======================

.. image:: https://travis-ci.org/jamespacileo/django-pure-pagination.svg?branch=master
    :target: https://travis-ci.org/jamespacileo/django-pure-pagination

Description
======================

:Author:
    James Pacileo `@ignighted <http://twitter.com/ignighted>`_

:Version:
    0.3.0

:Description:
    django-pure-pagination provides advanced pagination features and is fully compatible with existing code based on Django's core pagination module. (aka no need to rewrite code!)

:Requirements:
    Django 1.7+

:Contributors:
    `juandecarrion (Juande Carrion) <https://github.com/juandecarrion>`_, `twidi (Stéphane Angel) <https://github.com/twidi>`_, `bebraw (Juho Vepsäläinen) <https://github.com/bebraw>`_, `lampslave () <https://github.com/lampslave>`_, `GeyseR (Sergey Fursov) <https://github.com/GeyseR>`_, `zeus (Pavel Zhukov) <https://github.com/zeus>`_


Introduction
============

The django app offers advanced pagination features without forcing major code changes within an existing project.

Django-pure-pagination is based upon Django's core pagination module and is therefore compatible with the existing api.

`Documentation for Django core pagination module <http://docs.djangoproject.com/en/dev/topics/pagination/>`_

Features
--------

1. Uses same API as **django.core.pagination** and therefore is fully compatible with existing code.

2. Has dynamic query string creation, which takes into consideration existing GET parameters.

3. Out-of-the-box html rendering of the pagination

4. Additional methods make it easier to render more advanced pagination templates.


Installation
------------

Install package from PYPI:

::

    pip install django-pure-pagination

or clone and install from repository:

::

    git clone git@github.com:jamespacileo/django-pure-pagination.git
    cd django-pure-pagination
    python setup.py install

Add `pure_pagination` to INSTALLED_APPS

::

    INSTALLED_APPS = (
        ...
        'pure_pagination',
    )

Finally substitute **from django.core.paginator import Paginator** with **from pure_pagination import Paginator**

Settings
--------

A few settings can be set within settings.py

::

    PAGINATION_SETTINGS = {
        'PAGE_RANGE_DISPLAYED': 10,
        'MARGIN_PAGES_DISPLAYED': 2,

        'SHOW_FIRST_PAGE_WHEN_INVALID': True,
    }

**PAGE_RANGE_DISPLAYED** is the number of pages neighbouring the current page which will be displayed (default is 10)

**MARGIN_PAGES_DISPLAYED** is the number of pages neighbouring the first and last page which will be displayed (default is 2)

Set **SHOW_FIRST_PAGE_WHEN_INVALID** to True when you want to just show first page when provided invalid page instead of 404 error

.. image:: http://i.imgur.com/LCqrt.gif

Usage example
-------------

Following is a simple example for **function based views**. For generic class-based views, see bellow.

view file: **views.py**

::

    # views.py
    from django.shortcuts import render_to_response

    from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


    def index(request):

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(objects, request=request)

        people = p.page(page)

        return render_to_response('index.html', {
            'people': people,
        }


template file: **index.html**

::

    {# index.html #}
    {% extends 'base.html' %}

    {% block content %}

    {% for person in people.object_list %}
        <div>
            First name: {{ person }}
        </div>
    {% endfor %}

    {# The following renders the pagination html #}
    <div id="pagination">
        {{ people.render }}
    </div>

    {% endblock %}


Usage
-----

There a few different way you can make use of the features introduced within django-pure-pagination.

Easiest way to render the pagination is to call the render method i.e. **{{ page.render }}**

Alternatively you can access the Page object low level methods yourself

**Special note:** **page_obj** and **current_page** both point to the page object within the template.

::

    {% load i18n %}
    <div class="pagination">
        {% if page_obj.has_previous %}
            <a href="?{{ page_obj.previous_page_number.querystring }}" class="prev">&lsaquo;&lsaquo; {% trans "previous" %}</a>
        {% else %}
            <span class="disabled prev">&lsaquo;&lsaquo; {% trans "previous" %}</span>
        {% endif %}
        {% for page in page_obj.pages %}
            {% if page %}
                {% ifequal page page_obj.number %}
                    <span class="current page">{{ page }}</span>
                {% else %}
                    <a href="?{{ page.querystring }}" class="page">{{ page }}</a>
                {% endifequal %}
            {% else %}
                ...
            {% endif %}
        {% endfor %}
        {% if page_obj.has_next %}
            <a href="?{{ page_obj.next_page_number.querystring }}" class="next">{% trans "next" %} &rsaquo;&rsaquo;</a>
        {% else %}
            <span class="disabled next">{% trans "next" %} &rsaquo;&rsaquo;</span>
        {% endif %}
    </div>

Generic Class-Based Views
-------------------------

Documentation for Django generic class-based views on https://docs.djangoproject.com/en/dev/ref/class-based-views/


view file:

* **views.py**

    ::

        # views.py
        from django.views.generic import ListView

        from pure_pagination.mixins import PaginationMixin

        from my_app.models import MyModel


        class MyModelListView(PaginationMixin, ListView):
            # Important, this tells the ListView class we are paginating
            paginate_by = 10

            # Replace it for your model or use the queryset attribute instead
            object = MyModel

template files:

Note that the Django generic-based list view will include the object **page_obj** in the context. More information on https://docs.djangoproject.com/en/dev/ref/generic-views/#list-detail-generic-views

* **_pagination.html**

    ::

        {% load i18n %}
        <div class="pagination">
            {% if page_obj.has_previous %}
                <a href="?{{ page_obj.previous_page_number.querystring }}" class="prev">&lsaquo;&lsaquo; {% trans "previous" %}</a>
            {% else %}
                <span class="disabled prev">&lsaquo;&lsaquo; {% trans "previous" %}</span>
            {% endif %}
            {% for page in page_obj.pages %}
                {% if page %}
                    {% ifequal page page_obj.number %}
                        <span class="current page">{{ page }}</span>
                    {% else %}
                        <a href="?{{ page.querystring }}" class="page">{{ page }}</a>
                    {% endifequal %}
                {% else %}
                    ...
                {% endif %}
            {% endfor %}
            {% if page_obj.has_next %}
                <a href="?{{ page_obj.next_page_number.querystring }}" class="next">{% trans "next" %} &rsaquo;&rsaquo;</a>
            {% else %}
                <span class="disabled next">{% trans "next" %} &rsaquo;&rsaquo;</span>
            {% endif %}
        </div>

*  **my_app/myobject_list.html**

    ::

        {# my_app/myobject_list.html #}
        {% extends 'base.html' %}

        {% block content %}

        {% for object in object_list %}
            <div>
                First name: {{ object.first_name }}
            </div>
        {% endfor %}

        {# The following renders the pagination html #}
        {% include "_pagination.html" %}

        {% endblock %}
