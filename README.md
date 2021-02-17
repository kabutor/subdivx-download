A fork of Martín Gaitán's fork of Michel Peterson's subdivx.com-subtitle-retriever
Retrieve the best matching subtitle (in spanish) for a show episode from subdivx.com

Python3 version wasn't working, I just fixed for the actual website (subdivx.com) 

Also added these features:

- Unpack rared (rar5+ file format) subtitles beside zipped ones

Install
-------
```
$ git clone https://github.com/kabutor/subdivx-download
python3 setup.py 
```

My recomendation is to use a virtual env and install it there:

```
mkdir subs
python3 -m venv subs
source subs/bin/activate
then clone with git and install with all the dependencies
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
