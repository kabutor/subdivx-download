#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup

long_description = open('README.rst').read()

setup(
    name = 'subdivx-download',
    version = '0.2.1',
    description = 'A program to retrieve the best matching subtitle from subdivx.com',
    long_description = long_description,
    author = u'Michel Peterson. Modified by Martin Gaitan',
    author_email = 'michel@peterson.com.ar',
    url='https://github.com/nqnwebs/subdivx.com-subtitle-retriever',
    packages = ['subdivx_download',],
    license = 'GNU GENERAL PUBLIC LICENCE v3.0',
    install_requires = ['BeautifulSoup', 'tvnamer'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
    scripts = ['bin/subdivx-download'],
    
)
