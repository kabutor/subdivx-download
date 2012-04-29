#!/bin/env python

import os
import logging
import argparse
import logging.handlers

import subdivxlib as lib

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help="The series episode identifier to be downloaded")
    parser.add_argument('series_name', type=str, help="The name of the series subs to be downloaded")
    parser.add_argument('series_id', type=str, help="The series episode identifier to be downloaded")
    parser.add_argument('series_quality', type=str, help="The series episode quality to be downloaded")
    parser.add_argument('--quiet', '-q', action='store_true')

    args = parser.parse_args()

    lib.setup_logger(lib.LOGGER_LEVEL)

    if not args.quiet:
        console = logging.StreamHandler()
        console.setFormatter(lib.LOGGER_FORMATTER)
        lib.logger.addHandler(console)
    try:
        url = lib.get_subtitle_url(args.series_name, args.series_id, args.series_quality)
    except lib.NoResultsError, e:
        lib.logger.error(e.message)
        raise

    out_file_name = '/%s %s %s' % (args.series_name, args.series_id, args.series_quality)
    lib.get_subtitle(url, os.path.abspath(args.path) + out_file_name)


if __name__ == '__main__':
    main()
