#!/bin/env python

import os
import re
import logging
import argparse
import logging.handlers
from tvnamer.utils import FileParser
import subdivxlib as lib

#obtained from http://flexget.com/wiki/Plugins/quality
_qualities = ('1080i', '1080p', '1080p1080', '10bit', '1280x720',
              '1920x1080', '360p', '368p', '480', '480p', '576p',
               '720i', '720p', 'bdrip', 'brrip', 'bdscr', 'bluray',
               'blurayrip', 'cam', 'dl', 'dsrdsrip', 'dvb', 'dvdrip',
               'dvdripdvd', 'dvdscr', 'hdtv', 'hr', 'ppvrip',
               'preair', 'r5', 'rc', 'sdtvpdtv', 'tc', 'tvrip',
               'web', 'web-dl', 'web-dlwebdl', 'webrip', 'workprint')
_groups = ('2hd', 'asap', 'axxo', 'crimson', 'ctu', 'dimension', 'ebp',
           'fanta', 'fov', 'fqm', 'ftv', 'immerse', 'loki', 'lol',
           'notv', 'sfm', 'sparks')
_codecs = ('xvid', 'x264')

def extract_meta_data(filename):
    f = filename.lower()[:-4]
    def _match(options):
        try:
            match = [option for option in options if option in f][0]
        except IndexError:
            match = None
        return match
    quality = _match(_qualities)
    group = _match(_groups)
    codec = _match(_codecs)
    return quality, group, codec


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help="file(s) to retrieve subtitles")
    parser.add_argument('--quiet', '-q', action='store_true')

    args = parser.parse_args()

    lib.setup_logger(lib.LOGGER_LEVEL)

    if not args.quiet:
        console = logging.StreamHandler()
        console.setFormatter(lib.LOGGER_FORMATTER)
        lib.logger.addHandler(console)
    try:
        info = FileParser(args.path).parse()
        series_name = info.seriesname
        series_id = 's%02de%s' % (info.seasonnumber, '-'.join(['%02d' % e for e in info.episodenumbers]))
        quality, group, codec = extract_meta_data(args.path)
        url = lib.get_subtitle_url(series_name, series_id, group)
    except lib.NoResultsError, e:
        lib.logger.error(e.message)
        raise

    lib.get_subtitle(url, args.path[:-3] + 'srt' )


if __name__ == '__main__':
    main()
