#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

long_description = open('README.md').read() + '\n' + open('HISTORY.md').read()

setup(
    name='subdivx-download',
    version='0.5',
    description='A command line tool to download the best matching subtitle from subdivx.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=u"Martin Gaitán",
    author_email='gaitan@gmail.com',
    url='https://github.com/mgaitan/subdivx-download',
    packages=['subdivx',],
    license='GNU GENERAL PUBLIC LICENCE v3.0',
    install_requires=['beautifulsoup4', 'tvnamer'],
    entry_points={
        'console_scripts': ['subdivx=subdivx.cli:main'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
