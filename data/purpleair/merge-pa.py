"""
A simple script to merge purple-air Files
and create a CSV for our datamodel
"""

import os
import pandas as pd
import logging

logging.basicConfig(filename='import-data.log',
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] >> %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p')

logging.info('Starting an import job for PurpleAir data')
logging.info('OS current directory {}'.format(os.getcwd()))

folder = 'sample'

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

df=None

for file in buildListFromFiles(folder):
    file = os.path.join(folder, file)
    if not isinstance(df, type(None)):
        logging.info('Merging file {}'.format(file))
        df = df.append(getFileData(file), ignore_index = True)
    else:
        logging.info('Creating with first file {}'.format(file))
        df = getFileData(file)

df.to_csv("merged.csv", index=False)
