django-pure-pagination
======================

This django app is meant to pagination capabilities without enforcing code changes within a Django app.

The app is based upon the Django core pagination module.

Installation
------------

Add `purepagination` to INSTALLED_APPS

:

    INSTALLED_APPS = (
        ...
        'pure_pagination',
    )

Substitute `from django.core.paginator import Paginator` with `from purepagination.pagination import Paginator`

Usage
-----

There a few different way you can make use of the features introduced within django-pure-pagination.

Easiest way to render the pagination is to call the render method i.e. `{{ page.render }}`

Alternatively you can access the Page object low level methods yourself

:

    {% load i18n %}
    <div class="pagination">
        {% if current_page.has_previous %}
            <a href="?{{ current_page.previous_page_number.querystring }}" class="prev">&lsaquo;&lsaquo; {% trans "previous" %}</a>
        {% else %}
            <span class="disabled prev">&lsaquo;&lsaquo; {% trans "previous" %}</span>
        {% endif %}
        {% for page in current_page.pages %}
            {% if page %}
                {% ifequal page current_page.number %}
                    <span class="current page">{{ page }}</span>
                {% else %}
                    <a href="?{{ page.querystring }}" class="page">{{ page }}</a>
                {% endifequal %}
            {% else %}
                ...
            {% endif %}
        {% endfor %}
        {% if current_page.has_next %}
            <a href="?{{ current_page.next_page_number.querystring }}" class="next">{% trans "next" %} &rsaquo;&rsaquo;</a>
        {% else %}
            <span class="disabled next">{% trans "next" %} &rsaquo;&rsaquo;</span>
        {% endif %}
    </div>

