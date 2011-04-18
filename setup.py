import os
from distutils.core import setup
from setuptools import setup, find_packages

setup(name='django-pure-pagination',
      version='0.1',
      author='James Pacileo',
      license='BSD',
      keywords='pagination, django',
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Framework :: Django",
          "Environment :: Web Environment",
      ],
      author_email='jamespacileo@gmail.com',
      url='https://github.com/jamespacileo/django-pure-pagination/',
      #packages=['pure_pagination'],
      packages = ['pure_pagination'],# find_packages(exclude=['example_project']),
      include_package_data=True,
      #data_files = os.walk('pure_pagination'),
      zip_safe = False,
      package_data = {
        'pure_pagination': ['pure_pagination/templates', 'pure_pagination/templates/pure_pagination', 'pure_pagination/templates/pure_pagination/index.html'],
      },
      )