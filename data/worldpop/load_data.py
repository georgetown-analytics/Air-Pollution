
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

import pandas as pd

from osgeo import gdal

#import gdal
import os
from gdalconst import GA_ReadOnly
from ftplib import FTP
import os
from wpgpDownload.utils.wpcsv import Product
#from wpgpDownload.utils.wpcsv import ISO_LIST
import logging


logging.basicConfig(filename='import-data.log',
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] >> %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p')

logging.info('Starting an import job for WorlPop data')
logging.info('OS current directory {}'.format(os.getcwd()))

iso_country = 'USA'
USA_products = Product(iso_country)  # Where instead of GRC it could be any valid ISO code.


def load(ftpURL, ftpFilePath):
    logging.info('Load FTP fie without auth ({} fromm {})'.format(ftpURL, ftpFilePath))
    logging.info('OS current directory {}'.format(os.getcwd()))
    ftp = FTP(ftpURL)
    r = ftp.login()
    logging.info('FTP login response: {}'.format(r))
    relativeFilename = './' + ftpFilePath
    if not os.path.exists(os.path.dirname(relativeFilename)):
        try:
            os.makedirs(os.path.dirname(relativeFilename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    logging.info('FTP CWD change to: {}'.format(os.path.dirname(ftpFilePath)))
    ftp.cwd(os.path.dirname(ftpFilePath))
    ftp.retrlines('LIST', logging.info)

    with open(relativeFilename, 'wb') as f:
        ftp.retrbinary("RETR {}".format(os.path.basename(ftpFilePath)), f.write)

    ftp.quit()

worldpopManifest = "assets/wpgpDatasets.csv"
worldpopftp = "ftp.worldpop.org.uk"

logging.info('Load last version of worldpop manifest ({} fromm {})'.format(worldpopftp, worldpopManifest))
load(worldpopftp, worldpopManifest)



dfManifest=pd.read_csv('./' + worldpopManifest)
is_USA = dfManifest["ISO3"] == "USA"
USA_manifest = dfManifest[is_USA]

csv_to_update = 'bigtable.csv'
csv_template = '1km_t0.csv'
df_template=pd.read_csv(csv_template)
df_bigtable=pd.read_csv(csv_to_update)



buffer_deg=0.0027
xmax_MetroArea = -76.3881880661718 + buffer_deg
ymax_MetroArea = 39.5284754397557 + buffer_deg
xmin_MetroArea = -77.7356609923511 - buffer_deg
ymin_MetroArea = 38.3969644315365 - buffer_deg
extent = [xmin_MetroArea, ymax_MetroArea, xmax_MetroArea, ymin_MetroArea]
skip_if_DC_file_is_here = True

for Covariate_key, config in config_worldpop.items():
    logging.info('import job of {} convariate'.format(Covariate_key))
    date_filter=config["date"].rstrip('*')
    h24_filter=config["24hour"]
    column_name=config["column"]
    logging.info('Column {} using date filter {} wit hour filter {}'.format(column_name, date_filter, h24_filter))

    filePath = USA_manifest[USA_manifest["Covariate"]==Covariate_key]["PathToRaster"].iloc[0]
    logging.info('filePath FTP from manifest is {}'.format(filePath))
    bigTiff = './' + filePath
    DCtiff = "{}/DC_{}".format(os.path.dirname(bigTiff),os.path.basename(bigTiff))

    if (skip_if_DC_file_is_here and os.path.exists(DCtiff)):
        logging.info("We skip download of source tiff. DCtiff {} already here and skip is activated.".format(DCtiff))
    else:
        #download by FTP the big tiff
        load(worldpopftp, filePath)

        #clip and keep metro area tiff
        data = gdal.Open(bigTiff, GA_ReadOnly)
        logging.info("bigTiff: {}".format(bigTiff))
        logging.info("DCtiff: {}".format(DCtiff))
        #https://gdal.org/programs/gdal_translate.html
        data = None
        data = gdal.Open(bigTiff)
        data = gdal.Translate(DCtiff, data, projWin = extent)
        data = None
        logging.info("DC area tiff clip done")

    #delete big tiff
    if os.path.exists(bigTiff):
        os.remove(bigTiff)
    else:
        logging.warning('Original big tiff file {} not deleted, file not found.'.format(bigTiff))

    #update column values, create new line if no update available
    driver = gdal.GetDriverByName('GTiff')
    dataset = gdal.Open(DCtiff)
    band = dataset.GetRasterBand(1)
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    transform = dataset.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = -transform[5]

    data = band.ReadAsArray(0, 0, cols, rows)
    coordinates = df_template[['x', 'y', 'fid']].apply(tuple, axis=1).tolist()
    #get list of 25k coordinates tuples as [(-77.7356609923511, 39.5284754397557), (-77.7266778395099, 39.5284754397557), ...
    #import pdb; pdb. set_trace()
    #points_list = [ (355278.165927, 4473095.13829), (355978.319525, 4472871.11636) ] #list of X,Y coordinates
    #value = []
    if False:
        updated,created=0,0
        logging.info("CSV len {} before update".format(len(df_bigtable)))
        for point in coordinates:
            col = int((point[0] - xOrigin) / pixelWidth)
            row = int((yOrigin - point[1] ) / pixelHeight)
            #print ("{},{}={}".format(row, col, data[row][col]))
            #value += [data[row][col]]
            value = data[row][col]
            filtering=((df_bigtable['fid']==point[2])
                        & (df_bigtable['date'].str.startswith(date_filter, na=False)))
            if(date_filter == '2011-'):
                pass
                #import pdb; pdb. set_trace()
            if len(df_bigtable.loc[filtering]) > 0:
                #update existing rows
                logging.debug('Updating CSV {} row(s) for coord{}/{} @{}, column {} => {}'.format(len(df_bigtable.loc[filtering]),point[0],point[1],date_filter,column_name,value))
                df_bigtable.loc[filtering, column_name]=value
                updated += len(df_bigtable.loc[filtering])
            else:
                #add a new row with wildcards*
                logging.debug('Appending 1 row in CSV for coord{}/{} @{}, column {} => {}'.format(point[0],point[1],date_filter,column_name,value))
                df_bigtable=df_bigtable.append({'fid':point[2],'x':point[0],'y':point[1],'date':date_filter+'*','24hour':'*'},ignore_index=True)
                #import pdb; pdb. set_trace()
                created += 1
        logging.info("Saving CSV as {}".format(csv_to_update))
        logging.info("CSV len {}, {} created and {} updated".format(len(df_bigtable),created,updated))
        df_bigtable.to_csv(csv_to_update, index=False)
    #import pdb; pdb. set_trace()
