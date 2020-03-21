#!/usr/bin/env python

"""
Author julien collaer
Date 4/21/2020
Use: A simple command line tool to perform v1 worlpop data operations, using
the loader.py script functions.
Description: version 1, of a script to achieve first 2 steps of data sciece
pipeline:
* data extraction
* data wrangling
In order to make it possible in a local computer an exeption has been made add
the extracted data is clipped around DC reducing from 20Gb to 10Mb without
altering the DC area data.
In the v1 version we append data as feature for an already existing CSV file
of substations measurments.
"""

import os
import sys
import argparse
import logging
from loader import load

logging.basicConfig(filename='import-data.log',
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] >> %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p')


def main(arguments):
    logging.info('Starting an import job for Worldpop data')
    logging.info('OS current directory {}'.format(os.getcwd()))
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--folder", default='worldpop/GIS', type=str,
                        required=True, help="TMP_TIFF_FOLDER_NAME")
    parser.add_argument("--csv", default='bigtable.csv', type=str,
                        required=True, help="CSV_MERGED_FIlENAME")
    args = parser.parse_args(arguments)
    CSV_MERGED_FIlENAME = args.csv
    TMP_TIFF_FOLDER_NAME = args.folder
    logging.info('TMP_TIFF_FOLDER_NAME --folder: {}'.format(TMP_TIFF_FOLDER_NAME))
    logging.info('CSV_MERGED_FIlENAME --csv: {}'.format(CSV_MERGED_FIlENAME))
    load(CSV_MERGED_FIlENAME, TMP_TIFF_FOLDER_NAME)
    logging.info('========================FINISH=============================')


if __name__ == '__main__':
    logging.info('Direct main entry, runing main script')
    sys.exit(main(sys.argv[1:]))
