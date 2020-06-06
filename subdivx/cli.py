#!/bin/env python

import os
import logging
import argparse
from collections import namedtuple
import logging.handlers
from contextlib import contextmanager
from guessit import guessit
from tvnamer.utils import FileFinder
from . import lib

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
    'immerse',
    'internal',
    'ion10',
    'loki',
    'lol',
    'mement',
    'notv',
    'sfm',
    'sparks',
    'turbo'
)

_codecs = ('xvid', 'x264', 'h264', 'x265')


Metadata = namedtuple('Metadata', 'keywords quality codec')


def extract_meta_data(filename):
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
    parser.add_argument('--skip', '-s', type=int,
                        default=0, help="skip from head")
    parser.add_argument('--force', '-f', action='store_true',
                        default=False, help="override existing file")
    args = parser.parse_args()
    lib.setup_logger(lib.LOGGER_LEVEL)

    if not args.quiet:
        console = logging.StreamHandler()
        console.setFormatter(lib.LOGGER_FORMATTER)
        lib.logger.addHandler(console)

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
            number = f"s{info['season']:02}e{info['episode']:02}" if info["type"] == "episode" else info["year"]
            metadata = extract_meta_data(filename)

            url = lib.get_subtitle_url(
                info["title"], number,
                metadata,
                args.skip)
        except lib.NoResultsError as e:
            lib.logger.error(e.message)
            raise

        with subtitle_renamer(filepath):
            lib.get_subtitle(url, 'temp__' + filename )


if __name__ == '__main__':
    main()
