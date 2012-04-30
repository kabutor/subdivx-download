A fork of Michel Peterson's subdivx.com-subtitle-retriever
Retrieve the best matching subtitle (in spanish) for a show episode from subdivx.com

This fork simplify the way to use a stand-alone program, allowing
give a path (a filename or directory) as unique parameter.

Also added this features:

- Unpack rared subtitles beside zipped ones
- Better matching: look for *group* mention in subtitle description
- Rename subtitles after unpack it
- Packaging. pip installable ``setup.py`` and code modularized
- Can retrieve subtitles for a partially downloaded files (``*.part``, ``*.temp``, ``*.tmp``)

Install
-------

You can install it using pip::

    $ sudo pip install git+git://github.com/nqnwebs/h2dp


Usage
-----

usage: subdivx-download [-h] [--quiet] path

positional arguments:
  path         file or directory to retrieve subtitles

optional arguments:
  -h, --help   show this help message and exit
  --quiet, -q


.. tip::

    Run ``subdivx-download`` before ``tvnamer`` to give more metadata
    in your subtitle seach

