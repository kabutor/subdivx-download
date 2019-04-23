A fork of Michel Peterson's subdivx.com-subtitle-retriever
Retrieve the best matching subtitle (in spanish) for a show episode from subdivx.com

This fork simplify the way to use a stand-alone program, allowing
give a path (a filename or directory) as unique parameter and also changed
the algorithm to find the "best match" subtitle.

Also added these features:

- Unpack rared subtitles beside zipped ones
- Rename subtitles after unpack it
- Packaging. pip installable ``setup.py`` and code modularized
- Can retrieve subtitles for partially downloaded files (``*.part``, ``*.temp``, ``*.tmp``)

Install
-------

You can install it using pip:


```
$ pip3 install --user subdivx-download
```

or the development version:

```
$ pip3 install --user -U git+https://github.com/mgaitan/subdivx-download.git
```

Usage
-----


```
usage: subdivx [-h] [--quiet] [--skip SKIP] [--force] path

positional arguments:
  path                  file or directory to retrieve subtitles

optional arguments:
  -h, --help            show this help message and exit
  --quiet, -q
  --skip SKIP, -s SKIP  skip from head
  --force, -f           override existing file


.. tip::

    Run ``subdivx`` before ``tvnamer`` to give more metadata
    in your subtitle seach
```
