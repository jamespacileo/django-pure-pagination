import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-pure-pagination',
    version='0.3.0',
    url='https://github.com/jamespacileo/django-pure-pagination/',
    author='James Pacileo',
    author_email='jamespacileo@gmail.com',
    description='''django-pure-pagination provides advanced pagination features
                   and is fully compatible with existing code based on Django's
                   core 
                   pagination module. (aka no need to rewrite code!)''',
    long_description=README,
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords='pagination, django',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)