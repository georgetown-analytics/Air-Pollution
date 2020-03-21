#!/usr/bin/env python
"""
Author julien collaer
Date 4/21/2020
Use: don't use it directly, but use load-wp.py command line tool
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

import pandas as pd
from osgeo import gdal
import os
from gdalconst import GA_ReadOnly
from ftplib import FTP
from wpgpDownload.utils.convenience_functions import refresh_csv
refresh_csv()
from wpgpDownload.utils.wpcsv import Product
#from wpgpDownload.utils.wpcsv import ISO_LIST
import logging

config_worldpop = {
#'ppp_2010':{'column':'Population', 'date':'2010-*', '24hour':'*'},
#'ppp_2011':{'column':'Population', 'date':'2011-*', '24hour':'*'},
#'ppp_2012':{'column':'Population', 'date':'2012-*', '24hour':'*'},
#'ppp_2013':{'column':'Population', 'date':'2013-*', '24hour':'*'},
#'ppp_2014':{'column':'Population', 'date':'2014-*', '24hour':'*'},
#'ppp_2015':{'column':'Population', 'date':'2015-*', '24hour':'*'},
#'ppp_2016':{'column':'Population', 'date':'2016-*', '24hour':'*'},
#'ppp_2017':{'column':'Population', 'date':'2017-*', '24hour':'*'},
#'ppp_2018':{'column':'Population', 'date':'2018-*', '24hour':'*'},
'ppp_2019':{'column':'Population', 'date':'2019-*', '24hour':'*'},
#'ppp_2020':{'column':'Population', 'date':'2020-*', '24hour':'*'},
#'ppp_2020':{'column':'Road_density', 'date':'2020-*', '24hour':'*'},
#Distance to OSM major roads 2016
'osm_dst_road_100m_2016':{'column':'Dist-MRoads', 'date':'*', '24hour':'*'},
#Distance to interpolated built-settlement area edges 2010
#'dst_bsgme_100m_2010':{'column':'Dist-Setl', 'date':'2010-*', '24hour':'*'},
#'dst_bsgme_100m_2011':{'column':'Dist-Setl', 'date':'2011-*', '24hour':'*'},
#'dst_bsgme_100m_2012':{'column':'Dist-Setl', 'date':'2012-*', '24hour':'*'},
#'dst_bsgme_100m_2013':{'column':'Dist-Setl', 'date':'2013-*', '24hour':'*'},
#'dst_bsgme_100m_2014':{'column':'Dist-Setl', 'date':'2014-*', '24hour':'*'},
#'dst_bsgme_100m_2015':{'column':'Dist-Setl', 'date':'2015-*', '24hour':'*'},
#'dst_bsgme_100m_2016':{'column':'Dist-Setl', 'date':'2016-*', '24hour':'*'},
#'dst_bsgme_100m_2017':{'column':'Dist-Setl', 'date':'2017-*', '24hour':'*'},
#'dst_bsgme_100m_2018':{'column':'Dist-Setl', 'date':'2018-*', '24hour':'*'},
'dst_bsgme_100m_2019':{'column':'Dist-Setl', 'date':'2019-*', '24hour':'*'},
#'dst_bsgme_100m_2020':{'column':'Dist-Setl', 'date':'2020-*', '24hour':'*'},
#Distance to coastline 2000-2020
'dst_coastline_100m_2000_2020':{'column':'Dist-Coast', 'date':'*', '24hour':'*'},
#Distance to ESA-CCI-LC woody-tree area edges 2010
#'esaccilc_dst040_100m_2010':{'column':'Dist-Forest', 'date':'2010-*', '24hour':'*'},
#'esaccilc_dst040_100m_2011':{'column':'Dist-Forest', 'date':'2011-*', '24hour':'*'},
#'esaccilc_dst040_100m_2012':{'column':'Dist-Forest', 'date':'2012-*', '24hour':'*'},
#'esaccilc_dst040_100m_2013':{'column':'Dist-Forest', 'date':'2013-*', '24hour':'*'},
#'esaccilc_dst040_100m_2014':{'column':'Dist-Forest', 'date':'2014-*', '24hour':'*'},
#'esaccilc_dst040_100m_2015':{'column':'Dist-Forest', 'date':'2015-*', '24hour':'*'},
#'esaccilc_dst040_100m_2016':{'column':'Dist-Forest', 'date':'2016-*', '24hour':'*'},
#'esaccilc_dst040_100m_2017':{'column':'Dist-Forest', 'date':'2017-*', '24hour':'*'},
#'esaccilc_dst040_100m_2018':{'column':'Dist-Forest', 'date':'2018-*', '24hour':'*'},
'esaccilc_dst040_100m_2015':{'column':'Dist-Forest', 'date':'2019-*', '24hour':'*'},
#'esaccilc_dst040_100m_2020':{'column':'Dist-Forest', 'date':'2020-*', '24hour':'*'},
#SRTM slope 2000
'srtm_slope_100m':{'column':'Slope', 'date':'*', '24hour':'*'},
#SRTM elevation 2000
'srtm_topo_100m':{'column':'Elevation', 'date':'*', '24hour':'*'}
}
worldpopftp = "ftp.worldpop.org.uk"


logging.basicConfig(filename='import-data.log',
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] >> %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p')

logging.info('Starting an import job for WorlPop data')
logging.info('OS current directory {}'.format(os.getcwd()))


def getUSAProducts():
    iso_country = 'USA'
    USA_products = Product(iso_country)
    return pd.DataFrame(USA_products,
                        columns = ['idx', 'numeric', 'alpha3', 'country_name',
                                   'dataset_name', 'description', 'path'])


"""
Main function download data product manifest from worldpop
Iterate from onfig object the file to download
Compute and store results into the CSV file
"""
def load(CSV_MERGED_FIlENAME, TMP_TIFF_FOLDER_NAME, DONT_RELOAD_TIFF=True):
    USA_products = getUSAProducts()
    for Covariate_key, config in config_worldpop.items():
        logging.info('import job of {} covariate key'.format(Covariate_key))
        date_filter=config["date"].rstrip('*')
        h24_filter=config["24hour"]
        column_name=config["column"]
        logging.info('Column {} using date filter {}'.format(column_name, date_filter))
        if len(USA_products[USA_products["dataset_name"]==Covariate_key]["path"]) == 1:
            filePath = str(USA_products[USA_products["dataset_name"]==Covariate_key]["path"].iloc[0])
            logging.info('filePath FTP from manifest is {}'.format(filePath))
            addFeature(column_name, date_filter, CSV_MERGED_FIlENAME, TMP_TIFF_FOLDER_NAME, filePath, DONT_RELOAD_TIFF)
        else:
            logging.error('Error covariate key not found in manifest for {}'.format(Covariate_key))

"""
Add a feature to the big CSV by adding a column of column_name
In the specified CSV file CSV_MERGED_FIlENAME
From the worldpop tiff file in filePath
After getting and clipping the tiff it will be stored in TMP_TIFF_FOLDER_NAME
"""
def addFeature(column_name, date_filter, CSV_MERGED_FIlENAME, TMP_TIFF_FOLDER_NAME, filePath, DONT_RELOAD_TIFF):
    logging.info('**** add feature {} from {}'.format(column_name, filePath))
    DCtiff = getDCFile(filePath, TMP_TIFF_FOLDER_NAME, DONT_RELOAD_TIFF)
    geoTiffReader= geotiffReader(DCtiff)
    df = pd.read_csv(CSV_MERGED_FIlENAME)
    #Get all differents coordinates with id
    coordinates = df[['x', 'y', 'station_id']].apply(tuple, axis=1).tolist()
    # Get unique tuples from list using set() + list()
    coordinates = list(set(coordinates))
    logging.info('there is {} differents stations points for adding a feature'.format(len(coordinates)))
    for point in coordinates:
        tiffValue = geoTiffReader.getPixelValue(point[1], point[0])
        filter = ((df['station_id'] == point[2]) &
                  (df["datetime"].str.startswith(date_filter.rstrip('*'), na=False)))
        df.loc[filter, column_name]=tiffValue
    df.to_csv(CSV_MERGED_FIlENAME, index=False)

class geotiffReader(object):
    """Initialize a simple geotiff reader using gdal"""

    def __init__(self, DCtiff):
        self.DCtiff = DCtiff
        self.driver = gdal.GetDriverByName('GTiff')
        self.dataset = gdal.Open(self.DCtiff)
        self.band = self.dataset.GetRasterBand(1)
        self.cols = self.dataset.RasterXSize
        self.rows = self.dataset.RasterYSize
        self.transform = self.dataset.GetGeoTransform()
        self.xOrigin = self.transform[0]
        self.yOrigin = self.transform[3]
        self.pixelWidth = self.transform[1]
        self.pixelHeight = -self.transform[5]
        self.data = self.band.ReadAsArray(0, 0, self.cols, self.rows)
        logging.info('geotiff reader initiallized {}'.format(DCtiff))

    """
    Get geotiff value (one or first raster band)
    Worldpop get one one band ("grayscale tiff")
    Coordinates in degress WGS84 as the original tiff
    """
    def getPixelValue(self, x, y):
        col = int((x - self.xOrigin) / self.pixelWidth)
        row = int((self.yOrigin - y ) / self.pixelHeight)
        return self.data[row][col]


"""
Get specific tiff file filePath from Worldpop FTP
DONT_RELOAD_TIFF is True then dont download the file if already present
in TMP_TIFF_FOLDER_NAME folder
"""
def getDCFile(filePath, TMP_TIFF_FOLDER_NAME, DONT_RELOAD_TIFF):
    bigTiff = './' + TMP_TIFF_FOLDER_NAME + "/" + filePath
    DCtiff = "{}/DC_{}".format(os.path.dirname(bigTiff),os.path.basename(bigTiff))
    if (DONT_RELOAD_TIFF and os.path.exists(DCtiff)):
        logging.info("Skip tiff download. DC clipped tiff {} already dl and DONT_RELOAD_TIFF is activated.".format(DCtiff))
    else:
        #download by FTP the big tiff
        download(worldpopftp, filePath, bigTiff)
        clipDC(bigTiff, DCtiff)
    return DCtiff


"""
Clip a geoTiff to DC area using a small buffer in degree
"""
def clipDC(bigTiff, DCtiff):
    logging.info("bigTiff: {}".format(bigTiff))
    buffer_deg=0.0027
    xmax_MetroArea = -76.3881880661718 + buffer_deg
    ymax_MetroArea = 39.5284754397557 + buffer_deg
    xmin_MetroArea = -77.7356609923511 - buffer_deg
    ymin_MetroArea = 38.3969644315365 - buffer_deg
    extent = [xmin_MetroArea, ymax_MetroArea, xmax_MetroArea, ymin_MetroArea]
    data = gdal.Open(bigTiff, GA_ReadOnly)
    logging.info("{} geotiff opened byGDAL.".format(bigTiff))
    #https://gdal.org/programs/gdal_translate.html
    data = gdal.Translate(DCtiff, data, projWin = extent)
    data = None
    logging.info("DCtiff {} clipped and saved.".format(DCtiff))
    #delete big tiff
    if os.path.exists(bigTiff):
        os.remove(bigTiff)
        logging.info("Whole US tiff {} deleted.".format(bigTiff))


"""
Download from Worldpop FTP a file given his correct path.
FTP without authentication (open data)
"""
def download(ftpURL, ftpFilePat, bigTiff):
    logging.info('Load FTP file without auth ({} from {})'.format(ftpURL, ftpFilePath))
    logging.info('OS current directory {}'.format(os.getcwd()))
    ftp = FTP(ftpURL)
    r = ftp.login()
    logging.info('FTP login response: {}'.format(r))
    if not os.path.exists(os.path.dirname(bigTiff)):
        try:
            os.makedirs(os.path.dirname(bigTiff))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    logging.info('FTP CWD change to: {}'.format(os.path.dirname(ftpFilePath)))
    ftp.cwd(os.path.dirname(ftpFilePath))
    ftp.retrlines('LIST', logging.info)

    with open(bigTiff, 'wb') as f:
        ftp.retrbinary("RETR {}".format(os.path.basename(ftpFilePath)), f.write)
    ftp.quit()
