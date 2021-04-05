A fork of Martín Gaitán's fork of Michel Peterson's subdivx.com-subtitle-retriever
Retrieve the best matching subtitle (in spanish) for a show episode from subdivx.com

Python3 version wasn't working, I just fixed for the actual website (subdivx.com) 

Also added these features:

- Unpack rared (rar5+ file format) subtitles beside zipped and old rar version files
- Added option (-c) to manually choose wich subtitle to download 20210221
- Change the way links are used to UTF-8 to avoid weird characters bug 20210302
- When searching for a tvshow if the year is present it will use it also to improve search 20210321
- You can add keywords (-k) to improve the automatic selection among the subtitles available for a show. 05042021
- You can define the title of the show manually (-t) Useful when you have a folder with all the episodes titles, but not the show main title 06042021

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
  --choose, -c          show all the available subtitle and choose what to download
  --force, -f           override existing file
  --keyword -k "<string>" _ Add the <string> to the list of keywords. Keywords are used when you have 
  10 subtitles for a show or movie,and you know in the description there is a keyword for that subtitle.
  Example if rama966 is the creator of the subtitle you want to download, add it to the keyword and the 
  script will download that one. Combine -c with -k to see how subtitles are picked. 
  --title -t "<string>" _ Set the show main title to use instead of getting it from the file name


.. tip::
    If you want to look for a subtitle with an 's apostrophe, check that the file name is "zoey's.extraordinary.playlist.s01e01.mp4" 
    and no "zoeys.extraordinary.playlist.s01e01.mp4". Also you can remove the problematic words from the file name and leave it as
    "extraordinary.playlist.s01e04.mp4" and it may work.

    Run ``subdivx`` before ``tvnamer`` to give more metadata
    in your subtitle seach
```
