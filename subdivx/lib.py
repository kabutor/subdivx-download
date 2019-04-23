import requests
import logging
import logging.handlers
import os
import urllib.parse

from tempfile import NamedTemporaryFile
from zipfile import is_zipfile, ZipFile

from bs4 import BeautifulSoup

RAR_ID = b"Rar!\x1a\x07\x00"

SUBDIVX_SEARCH_URL = "https://www.subdivx.com/index.php?buscar=%s+%s&accion=5&masdesc=&subtitulos=1&realiza_b=1&oxdown=1"
SUBDIVX_DOWNLOAD_MATCHER = {'name':'a', 'rel':"nofollow", 'target': "new"}

LOGGER_LEVEL = logging.DEBUG
LOGGER_FORMATTER = logging.Formatter('%(asctime)-25s %(levelname)-8s %(name)-29s %(message)s', '%Y-%m-%d %H:%M:%S')

class NoResultsError(Exception):
    pass


def is_rarfile(fn):
    '''Check quickly whether file is rar archive.'''
    buf = open(fn, "rb").read(len(RAR_ID))
    return buf == RAR_ID


def setup_logger(level):
    global logger

    logger = logging.getLogger()

    logfile = logging.handlers.RotatingFileHandler(logger.name+'.log', maxBytes=1000 * 1024, backupCount=9)
    logfile.setFormatter(LOGGER_FORMATTER)
    logger.addHandler(logfile)
    logger.setLevel(level)


def get_subtitle_url(series_name, series_id, metadata, skip=0):
    enc_series_name = urllib.parse.quote(series_name)
    enc_series_id = urllib.parse.quote(series_id)

    logger.debug('Starting request to subdivx.com')
    url = SUBDIVX_SEARCH_URL % (enc_series_name, enc_series_id)
    page = requests.get(url).text
    logger.debug('Search Query URL: ' + url)
    soup = BeautifulSoup(page, 'html5lib')
    titles = soup('div', id='menu_detalle_buscador')

    # only include results for this specific serie / episode
    # ie. search terms are in the title of the result item
    descriptions = [
        title.nextSibling(id='buscador_detalle_sub')[0] for title in titles
        if series_name in title.text.lower() and series_id in title.text.lower()
    ]

    if not descriptions:
        raise(NoResultsError(' '.join(['No suitable subtitles were found for:',
                                      series_name,
                                      series_id]))
        )
    # then find the best result looking for metadata keywords in the description
    scores = []
    for description in descriptions:

        text = description.text
        score = 0
        for keyword in metadata.keywords:
            if keyword in text:
                score += 1
        for quality in metadata.quality:
            if quality in text:
                score += 1.1
        for codec in metadata.codec:
            if codec in text:
                score += .75
        scores.append(score)

    results = sorted(zip(descriptions, scores), key=lambda item: item[1], reverse=True)
    print(results[0][0].text)
    return results[0][0].nextSibling.find(**SUBDIVX_DOWNLOAD_MATCHER)['href']


def get_subtitle(url, path):
    temp_file = NamedTemporaryFile()
    temp_file.write(requests.get(url).content)
    temp_file.seek(0)

    if is_zipfile(temp_file.name):
        zip_file = ZipFile(temp_file)
        for name in zip_file.namelist():
            # don't unzip stub __MACOSX folders
            if '.srt' in name and '__MACOSX' not in name:
                logger.info(' '.join(['Unpacking zipped subtitle', name, 'to', os.path.dirname(path)]))
                zip_file.extract(name, os.path.dirname(path))

        zip_file.close()

    elif is_rarfile(temp_file.name):
        rar_path = path + '.rar'
        logger.info('Saving rared subtitle as %s' % rar_path)
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
    temp_file.close()
