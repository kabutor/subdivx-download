***News on 16 March 2024***

As of march 2024 I realized that this stopped working, I went to the subdivx.com site and it has changed, a lot, so this stopped working until now, this is now working, probably there are some problems still that need to be fixed, and I want to make the chrome headless, but for now it's working.

I was trying to fix, doing small changes, but soon I realized that the new site is full of javascript, the old python request module wasn't gonna do the trick anymore, time to draw the big guns, Selenium and make it work again.

The only file you need now is the subdix.py file, ***you have to create a folder named "down" and set the full path in the first lines of the subdivx.py file***, and run it as before and the subtitle should be downloaded and renamed. That folder has to be empty always, it will be used to download the sub file, uncompress it and then delete it.
```
subdivx.py Lucifer.s01e01.hdtv.mkv
    0 Mar 15 11:46 Lucifer.s01e01.hdtv.mkv
59533 Aug 12  2015 Lucifer.s01e01.hdtv.srt
```

Dependencies you need to install 

guessit

html5lib

tvnamer

beautifulsoup4

python3-selenium  (tested with 4.18.1)

chromium-driver





========= OLD INSTRUCTIONS BELOW ================== just keeping them until I'm confident on deleting this

A fork of Martín Gaitán's fork of Michel Peterson's subdivx.com-subtitle-retriever
Retrieve the best matching subtitle (in spanish) for a show episode from subdivx.com

Python3 version wasn't working, I just fixed for the actual website (subdivx.com)

Also added these features:

- Unpack rared (rar5+ file format) subtitles beside zipped and old rar version files
- Added option (-c) to manually choose wich subtitle to download 20210221
- Change the way links are used to UTF-8 to avoid weird characters bug 20210302
- <strike>When searching for a tvshow if the year is present it will use it also to improve search 20210321</strike> removed as 20210701
- You can add keywords (-k) to improve the automatic selection among the subtitles available for a show. 20210405
- You can define the title of the show manually (-t) Useful when you have a folder with all the episodes titles, but not the show main title 20210406
- If no subtitle is available, program will continue for next title (in case you try to download several episodes with one command), also the message in case of error is better explained 20211018

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
then clone with git and install with all the dependencies among them:
pip install guessit
pip install html5lib
pip install tvnamer
pip install beautifulsoup4
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
    Also can use the -t option to set the name, and then use the apostrophe escaped (\')

```
