"""
A simple script to merge purple-air Files
and create a CSV for our datamodel
"""

import os
import sys
import argparse
import pandas as pd
import logging

logging.basicConfig(filename='import-data.log',
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] >> %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p')

logging.info('Starting an import job for PurpleAir data')
logging.info('OS current directory {}'.format(os.getcwd()))


"""
create a list of all relevant primary CSV files from purple Air
from a given folder
"""
def buildListFromFiles(folder):
    filesList = []
    for file in os.listdir(folder):
        logging.info('Hiting file {}'.format(file))
        if file.endswith(".csv") and ('Primary' in file):
            logging.info('Adding file {} to list'.format(file))
            filesList += [file]
    return filesList

def getFileData(file):
    df = pd.read_csv(file)
    columns = list(df.columns)
    columns.remove("created_at")
    columns.remove("PM2.5_ATM_ug/m3")
    #import pdb; pdb.set_trace()
    df = df.rename(columns={"PM2.5_ATM_ug/m3": "pm25", "created_at":"datetime"})
    df = df.drop(columns, axis=1)
    df['type'] = "PurpleAir"
    if " B " in file:
        df['sensor'] = "B"
    else:
        df['sensor'] = "A"
    df['station_id'] = os.path.basename(file)
    x = os.path.basename(file).split("(")[2].split(")")[0].split(" ")[0]
    y = os.path.basename(file).split("(")[2].split(")")[0].split(" ")[1]
    df["x"] = x
    df["y"] = y
    return df


def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--folder", default='purpleair/sample', type=str,
                        required=False, help="CSV_FOLDER_NAME")
    parser.add_argument("--csv", default='bigtable.csv', type=str,
                        required=False, help="CSV_MERGED_FIlENAME")
    args = parser.parse_args(arguments)
    CSV_MERGED_FIlENAME = args.csv
    CSV_FOLDER_NAME = args.folder
    df=None
    for file in buildListFromFiles(CSV_FOLDER_NAME):
        file = os.path.join(CSV_FOLDER_NAME, file)
        if not isinstance(df, type(None)):
            logging.info('Merging file {}'.format(file))
            df = df.append(getFileData(file), ignore_index = True)
        else:
            logging.info('Creating with first file {}'.format(file))
            df = getFileData(file)

    df.to_csv(CSV_MERGED_FIlENAME, index=False)

if __name__ == '__main__':
    logging.info('Direct main entry, runing main script')
    sys.exit(main(sys.argv[1:]))
