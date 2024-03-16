#!/bin/env python
from selenium import webdriver                                                                                                       
from selenium.webdriver.chrome.service import Service                                                                                
#import undetected_chromedriver as uc                             
from selenium.webdriver.common.by import By                       
from selenium.webdriver.support.ui import WebDriverWait      
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.keys import Keys
import os
import logging
import argparse
from collections import namedtuple
import logging.handlers
from contextlib import contextmanager
from guessit import guessit
from tvnamer.utils import FileFinder
import requests 
import logging.handlers
import urllib.parse

from tempfile import NamedTemporaryFile
from zipfile import is_zipfile, ZipFile

from bs4 import BeautifulSoup
import time
import re, os

# download path set, need to be full path
download_path = os.path.join(os.getcwd(), "down")
# check if download path is empty
if (len(os.listdir(download_path)) > 0 and (os.path.isdir(download_path))):
    print("Download folder ./down not Empty or exist")
    quit()

PYTHONUTF8=1

RAR_ID = b"Rar!\x1a\x07\x00"
RAR5_ID = b"Rar!\x1A\x07\x01\x00"

SUBDIVX_SEARCH_URL = "https://www.subdivx.com/inc/ajax.php"


SUBDIVX_DOWNLOAD_MATCHER = {'name':'a', 'rel':"nofollow", 'target': "new"}

LOGGER_LEVEL = logging.INFO
LOGGER_FORMATTER = logging.Formatter('%(asctime)-25s %(levelname)-8s %(name)-29s %(message)s', '%Y-%m-%d %H:%M:%S')

# Start Selenium
service = Service(executable_path="/usr/bin/chromedriver")
op = webdriver.ChromeOptions()
prefs = {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False}
op.add_experimental_option('prefs', prefs)
#op.add_argument("download.default_directory=./down")

PROXY="http://127.0.0.1:8080"
#op.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome(service=service, options=op)
#options=op)
driver.implicitly_wait(3)
driver.set_window_size(1280,1024)


#s.headers.update({"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",                  "accept-encoding":"gzip, deflate, br", 
#                  "accept-language":"es-ES;es;q=0.9;en;q=0.8"
#                  })

# init browser
driver.get("https://www.subdivx.com/index.php" )

#driver.get("https://www.subdivx.com/paginas/resultados.php", verify=False )
#driver.get("https://www.subdivx.com/paginas/navbar.php", verify=False )

class NoResultsError(Exception):
    pass


def is_rarfile(fn):
    '''Check quickly whether file is rar archive.'''
    buf = open(fn, "rb").read(len(RAR_ID))
    #print (buf)
    return buf == RAR_ID

def is_rar5file(fn):
    '''Check quickly whether file is rar5 archive.'''
    buf = open(fn, "rb").read(len(RAR5_ID))
    #print (buf)
    return buf == RAR5_ID


def setup_logger(level):
    global logger

    logger = logging.getLogger()
    """
    logfile = logging.handlers.RotatingFileHandler(logger.name+'.log', maxBytes=1000 * 1024, backupCount=9)
    logfile.setFormatter(LOGGER_FORMATTER)
    logger.addHandler(logfile)
    """
    logger.setLevel(level)


def get_subtitle_down(title, number, metadata, choose=False):
    #Filter the title to avoid 's in names
    title_f = [ x for x in title.split() if "\'s" not in x ]
    title = ' '.join(title_f)
    buscar = f"{title} {number}"
    
    print(buscar)
    # wait until search box
    searchElement = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, '//*[@id="buscar"]')))
    searchElement.send_keys(buscar)
    searchElement.send_keys(Keys.RETURN)
    time.sleep(2)
    page = driver.page_source.encode('utf-8')
    #page = .post(SUBDIVX_SEARCH_URL, params=params, verify=False).text
    soup = BeautifulSoup(page, 'html5lib')
    titles = soup.find_all("tr",attrs={'class': re.compile('^trMarcar.*')}) 
    
    # only include results for this specific serie / episode
    # ie. search terms are in the title of the result item
    '''
    descriptions = {
        t.nextSibling(id='buscador_detalle_sub')[0].text: t.next('a')[0]['href'] for t in titles
        if all(word.lower() in t.text.lower() for word in buscar.split())
    }
    '''
    count = 1   # index of selenium search at 1 3 5 7 9 11 13 15 17
    descriptions = {}
    for t in titles:
        res = t.find("td", {"class":"align-middle text-white px-5 fw-bold dtr-hidden"})
        descriptions[str(count)] = res.text
        count+=2

    if not descriptions:
        raise NoResultsError(f'\033[31m[+]\033[0mNo suitable subtitles were found for: "{buscar}"')
    # then find the best result looking for metadata keywords
    # in the description
    scores = []
    for description in descriptions:
        score = 0
        for keyword in metadata.keywords:
            if keyword in description:
                score += 1
        for quality in metadata.quality:
            if quality in description:
                score += 1.1
        for codec in metadata.codec:
            if codec in description:
                score += .75
        scores.append(score)


    results = sorted(zip(descriptions.items(), scores), key=lambda item: item[1], reverse=True)
    
    if (choose):
        count = 0
        for item in (results):
            print ("\t \033[92m %i \033[0m %s" % (count , item[0][1]))
            count = count +1
        res = int(input ("Sub to download? (0)") or "0")
        url = results[res][0][0] 
    else:
        # get subtitle page
        url = results[0][0][0]
    
    # now search the elements on selenium
    clickElement = driver.find_element(By.CSS_SELECTOR,"#resultados > tbody > tr:nth-child(" + url + ")")
    clickElement.click()
    logger.info(f"Getting from {url}")
    downElement = driver.find_element(By.CSS_SELECTOR,"#btnDescargar")
    downElement.click()
    # TODO
    # c&p from stackoverflow to get the file name of the downloaded file
    '''
    filename = driver.execute_script("""
                var file_name = document.querySelector('downloads-manager')
                    .shadowRoot.getElementById('frb0')
                    .shadowRoot.getElementById('file-link').textContent;
                return file_name;
                """)
    print(filename)
    '''
    # wait for download
    time.sleep(3)
    filedown = os.listdir(download_path)
    return filedown[0] 


def get_subtitle(downfile, path):
    temp_file = NamedTemporaryFile()
    logger.info(f"opening {downfile}")
    with open(os.path.join(download_path,downfile), mode='rb') as f:
        contentfile = f.read()
        #delete file
        os.remove(os.path.join(download_path,downfile))

    temp_file.write(contentfile)
    temp_file.seek(0)
    
    if is_zipfile(temp_file.name):
        zip_file = ZipFile(temp_file)
        for name in zip_file.infolist():
            # don't unzip stub __MACOSX folders
            if '.srt' in name.filename and '__MACOSX' not in name.filename:
                logger.info(' '.join(['\033[32m[*]\033[0mUnpacking zipped subtitle', name.filename, 'to', os.path.dirname(path)]))
                zip_file.extract(name, os.path.dirname(path))

        zip_file.close()

    elif (is_rarfile(temp_file.name) or is_rar5file(temp_file.name)):
        rar_path = path + '.rar'
        logger.info('\033[32m[*]\033[0mSaving rared subtitle as %s' % rar_path)
        with open(rar_path, 'wb') as out_file:
            out_file.write(temp_file.read())

        try:
            import subprocess
            #extract all .srt in the rared file
            ret_code = subprocess.call(['unrar', 'e', '-n*srt', rar_path])
            if ret_code == 0:
                logger.info('Unpacking rared subtitle to %s' % os.path.dirname(path))
                os.remove(rar_path)
        except OSError:
            logger.info('Unpacking rared subtitle failed.'
                        'Please, install unrar to automate this step.')
    else:
        logger.info(f"unknown file type")


    temp_file.close()


_extensions = [
    'avi', 'mkv', 'mp4',
    'mpg', 'm4v', 'ogv',
    'vob', '3gp',
    'part', 'temp', 'tmp'
]

#obtained from http://flexget.com/wiki/Plugins/quality
_qualities = ('1080i', '1080p', '1080p1080', '10bit', '1280x720',
              '1920x1080', '360p', '368p', '480', '480p', '576p',
               '720i', '720p', 'bdrip', 'brrip', 'bdscr', 'bluray',
               'blurayrip', 'cam', 'dl', 'dsrdsrip', 'dvb', 'dvdrip',
               'dvdripdvd', 'dvdscr', 'hdtv', 'hr', 'ppvrip',
               'preair', 'r5', 'rc', 'sdtvpdtv', 'tc', 'tvrip',
               'web', 'web-dl', 'web-dlwebdl', 'webrip', 'workprint')
_keywords = (
    '2hd',
    'adrenaline',
    'amnz',
    'asap',
    'axxo',
    'compulsion',
    'crimson',
    'ctrlhd',
    'ctrlhd',
    'ctu',
    'dimension',
    'ebp',
    'ettv',
    'eztv',
    'fanta',
    'fov',
    'fqm',
    'ftv',
    'galaxyrg',
    'galaxytv',
    'hazmatt',
    'immerse',
    'internal',
    'ion10',
    'killers',
    'loki',
    'lol',
    'mement',
    'minx',
    'notv',
    'phoenix',
    'rarbg',
    'sfm',
    'sva',
    'sparks',
    'turbo'
)

_codecs = ('xvid', 'x264', 'h264', 'x265')


Metadata = namedtuple('Metadata', 'keywords quality codec')


def extract_meta_data(filename, kword):
    f = filename.lower()[:-4]
    def _match(options):
        try:
            matches = [option for option in options if option in f]
        except IndexError:
            matches = []
        return matches
    keywords = _match(_keywords)
    quality = _match(_qualities)
    codec = _match(_codecs)
    #Split keywords and add to the list
    if (kword):
        keywords = keywords + kword.split(' ')
    return Metadata(keywords, quality, codec)


@contextmanager
def subtitle_renamer(filepath):
    """dectect new subtitles files in a directory and rename with
       filepath basename"""

    def extract_name(filepath):
        filename, fileext = os.path.splitext(filepath)
        if fileext in ('.part', '.temp', '.tmp'):
            filename, fileext = os.path.splitext(filename)
        return filename

    dirpath = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    before = set(os.listdir(dirpath))
    yield
    after = set(os.listdir(dirpath))
    for new_file in after - before:
        if not new_file.lower().endswith('srt'):
            # only apply to subtitles
            continue
        filename = extract_name(filepath)
        os.rename(new_file, filename + '.srt')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str,
                        help="file or directory to retrieve subtitles")
    parser.add_argument('--quiet', '-q', action='store_true')
    parser.add_argument('--choose', '-c', action='store_true',
                        default=False, help="Choose sub manually")
    parser.add_argument('--force', '-f', action='store_true',
                        default=False, help="override existing file")
    parser.add_argument('--keyword','-k',type=str,help="Add keyword to search among subtitles")
    parser.add_argument('--title','-t',type=str,help="Set the title of the show")
    args = parser.parse_args()
    setup_logger(LOGGER_LEVEL)

    if not args.quiet:
        console = logging.StreamHandler()
        console.setFormatter(LOGGER_FORMATTER)
        logger.addHandler(console)

    cursor = FileFinder(args.path, with_extension=_extensions)

    for filepath in cursor.findFiles():
        # skip if a subtitle for this file exists
        sub_file = os.path.splitext(filepath)[0] + '.srt'
        if os.path.exists(sub_file):
            if args.force:
                os.remove(sub_file)
            else:
                continue

        filename = os.path.basename(filepath)
        
        try:
            info = guessit(filename)
            if 'season' in info:
                if (hasattr(info['season'], '__len__') and (not isinstance(info['season'], str)) ):
                    info['season'] = info['season'][0]
                number = f"s{info['season']:02}e{info['episode']:02}" if info["type"] == "episode" else info["year"]
            else:
                number = info["year"]
            metadata = extract_meta_data(filename, args.keyword)
            
            if (args.title):
                title=args.title
            else:
                title = info["title"]
            downfile = get_subtitle_down(
                title, number,
                metadata,
                args.choose)
        except NoResultsError as e:
            logger.error(str(e))
            downfile=''
        if(downfile !=''):
            with subtitle_renamer(filepath):
                get_subtitle(downfile, 'temp__' + filename )

if __name__ == '__main__':
    main()
