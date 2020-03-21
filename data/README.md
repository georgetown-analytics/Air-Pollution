# How to load the data

## Load base data from Groudstations

1. PurpleAir data

First step will create a new CSV file (**[CSV_MERGED_FIlENAME]**), from a folder of CSV files downloaded (**[CSV_FOLDER_NAME]**).
from openAQ.

For our DC metro area we used the download page here : https://www.purpleair.com/sensorlist?exclude=true&nwlat=38.94035140127292&selat=38.847757301908075&nwlng=-77.14710278732194&selng=-76.95675328903368

We configured it to download exclusively external sensors during a specific period of years and each 60minutes.

* Temporal resolution is very high and we limit it to 1 24hour
* spatial resolution is just one point for each ground station (just a few about 20 in DC metro area)

Note an API also exists, detail and doc here: https://docs.google.com/document/d/15ijz94dXJ-YAZLi9iZ_RaBwrZ4KtYeCy08goGBwnbCU/


From the ./Air-Pollution/data folder execute the script:
'''
# python purpleair/load-pa.py [CSV_FOLDER_NAME] [CSV_MERGED_FIlENAME]
'''

2. OpenAQ data

The goal is to add ore rows to the first openAQ data by downloading and apending rows to the previous CSV file (**[CSV_MERGED_FIlENAME]**)

@todo

3. Worldpop data

The goal of thisstep is to append columns or features to the previous CSV file (**[CSV_MERGED_FIlENAME]**) extracting data fron worldpop open data FTP.

Worldpop https://www.worldpop.org/, is a open data initiative using AI to compute a full coverage of world population but also provide other datas products that were used to compute this final result.

Worldpop provides geotiff file for each countries and sometimes yearly (population are provided for each year but distance to coast or slope are not year dependant).

* The spatial resolution is 100x100m
* The temporal resolution is year

The features :
* population by 100x100m (yearly data)
* distance to mains roads (absolute data from 2015)
* distance to forest (data between 2010 until 2015, years after 2015 will use 2015)
* distance to coast (absolute data)
* distance to settlement (data between 2010 until 2015, years after 2015 will use 2015)
* Slope
* Elevation

See jupyter notebook located in data/worldpop/exploring_population2013.ipynb for more details about the workflow logic of data extraction and mulching.

The goal of this script is to download the tiff files, clip them around the DC area (US tiff is about 20Gb each and DC <10Mb)

After it will get the value (pixel value from tiff) for each groundstation location by measurement year.

*You need pandas, wpgpDownload (worldpop python API available on github) and gdal python libraries installed.*

From the ./Air-Pollution/data folder execute the script:
'''
# python worldpop/load-wp.py [TMP_TIFF_FOLDER_NAME] [CSV_MERGED_FIlENAME]
'''

4. Meteorogical data

The goal is to continue addings rows/feature to the previousCSV file (**[CSV_MERGED_FIlENAME]**).
