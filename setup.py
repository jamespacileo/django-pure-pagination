import os
from distutils.core import setup
from setuptools import setup, find_packages

setup(name='django-pure-pagination',
      version='0.2',
      author='James Pacileo',
      long_description = open('README.rst').read(),
      license='BSD',
      keywords='pagination, django',
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 3",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Framework :: Django",
          "Environment :: Web Environment",
      ],
      author_email='jamespacileo@gmail.com',
      url='https://github.com/jamespacileo/django-pure-pagination/',
      packages = ['pure_pagination'],
      include_package_data=True,
      zip_safe = False,
      package_data = {
        'pure_pagination': ['pure_pagination/templates', 'pure_pagination/templates/pure_pagination', 'pure_pagination/templates/pure_pagination/index.html'],
      },
      )