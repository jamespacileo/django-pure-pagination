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
        'purepagination',
    )

Substitute `from django.core.paginator import Paginator` with `from purepagination.pagination import Paginator`

Usage
-----

There a few different way you can make use of the features introduced within django-pure-pagination.

Firstly you can just use the render the pagination html directly by using `{{ page.render_pagination }}`v

