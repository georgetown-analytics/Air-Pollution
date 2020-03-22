#!/usr/bin/env python

#https://ianlondon.github.io/blog/encoding-cyclical-features-24hour-time/
"""
Author julien collaer
Date 4/21/2020
Use: A simple command line tool to perform add cyclic value to a csv from
a colmn using a formatter interpretation string pattern
"""

import os
import sys
import argparse
import logging
#import datetime as dt
import pandas as pd
import numpy as np

logging.basicConfig(filename='import-data.log',
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] >> %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p')


def main(arguments):
    logging.info('****************************************')
    logging.info('        Starting a cyclic value')
    logging.info('****************************************')
    logging.info('OS current directory {}'.format(os.getcwd()))
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--column", default='datetime', type=str,
                        required=True, help="COLUMN_NAME")
    parser.add_argument("--dateformat", default='%Y-%m-%d %H:%M:%S %Z', type=str,
                        required=False, help="FORMAT date format")
    parser.add_argument("--csv", default='bigtable.csv', type=str,
                        required=True, help="CSV_MERGED_FIlENAME")
    args = parser.parse_args(arguments)
    CSV_MERGED_FIlENAME = args.csv
    FORMAT = args.dateformat
    COLUMN_NAME = args.column
    logging.info('COLUMN_NAME --column: {}'.format(COLUMN_NAME))
    logging.info('FORMAT --dateformat: {}'.format(FORMAT))
    logging.info('CSV_MERGED_FIlENAME --csv: {}'.format(CSV_MERGED_FIlENAME))
    cyclic(CSV_MERGED_FIlENAME, FORMAT, COLUMN_NAME)
    logging.info('========================FINISH=============================')


#https://stackoverflow.com/questions/54787146/get-the-time-spent-since-midnight-in-dataframe
def secSinceNoon(datTimStr):
    tt = pd.to_datetime(datTimStr).time()
    return tt.hour * 3600 + tt.minute * 60 + tt.second


def cyclic(CSV_MERGED_FIlENAME, FORMAT, COLUMN_NAME):
    df = pd.read_csv(CSV_MERGED_FIlENAME)
    #df['time'] = df[COLUMN_NAME].apply(lambda x: dt.datetime.strptime(x, FORMAT))
    df['time'] = pd.to_datetime(df[COLUMN_NAME],format=FORMAT)
    df['seconds'] = df.time.apply(secSinceNoon)
    df['days'] = pd.Series(df.time).dt.dayofyear
    df['dayofweek'] = pd.Series(df.time).dt.dayofweek
    seconds_in_day = 60*60*24
    days_in_year=365 #okay since it is for 2019 not odd year
    df['sin_day'] = np.sin(2*np.pi*df.seconds/seconds_in_day)
    df['cos_day'] = np.cos(2*np.pi*df.seconds/seconds_in_day)
    df['sin_year'] = np.sin(2*np.pi*df.days/days_in_year)
    df['cos_year'] = np.cos(2*np.pi*df.days/days_in_year)
    df['date'] = pd.Series(df.time).dt.strftime("%Y-%m-%d")
    df['24hr'] = pd.Series(df.time).dt.strftime("%I:%M:%S")
    df = df.drop(['time','seconds','days'], axis=1)
    df.to_csv(CSV_MERGED_FIlENAME, index=False)

if __name__ == '__main__':
    logging.info('Direct main entry, runing main script')
    sys.exit(main(sys.argv[1:]))
