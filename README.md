# Air-Pollution
Cohort 18 Capstone Project for the Certificate of Data Science at Georgetown University School of Continuing Studies.

The increase in fine particulate matter PM2.5 levels over the last 50 years has resulted in a significant decline in overall air quality for people living in urban hubs in the United States. The American Lung Association in their 2020 State of the Air study estimates that over 150 million people in the United States - 48.5% of the population - live in counties or zones with unhealthy air as measured by ozone concentrations and PM2.5 concentrations (2020). PM2.5, whose particle size is less than 2.5 microns in diameter, poses a significant health risk to overall public health. Due to its small size, these particles are dispersed widely and have the ability to enter deep into the lungs, and even the bloodstream causing a myriad of respiratory and cardiovascular issues such as increased respiratory problems, decreased lung function, asthma, irregular heartbeats, and premature death due to heart and lung disease (Environmental Protection Agency [EPA], 2020). Due to the seriousness of high PM2.5 levels, there is government monitoring of air pollution levels; however, a sparse network of air pollution monitors with infrequent data collection provide an incomplete analysis of air quality and begets the need for a more localized model. The ability to locate, measure, and predict PM2.5 levels is vital for protecting vulnerable populations within local communities. The goal of this study was to develop a high-resolution air pollution model which can predict air quality levels at hourly intervals providing residents in the District of Columbia a tool for making healthier decisions about where and when they spend their time outside.

Keywords:  PM2.5, Air Quality, Ozone Concentrations, Health, Deep Lungs and Bloodstream, Premature Death.


### Data Extract and Data Wrangling :

- /data/ folder Data extraction & wrangling.ipynb centralizes and executes all scripts from /worldpop, /purpleair, /openAQ /weather and /cyclic subfloders.

### Data Exploration, Vizualization, Analysis and model analysis

- /model/ folder, follow ordered notebooks

### App and Final Data Product

- /app/ folder, differents proofs of concept:
 - flask app in app folder
 - Streamlit
 - Tableau
 - Web Javascript (no server side computation) in /app/test/ subfolder

*Web app prototype hosted on github here:*

[![AirQuality Prototype App](/app/test/airquality-prototype-app.png)](https://collaer.github.io/simplemap/Air-Pollution/app/)

If gh-pages is opened in this repo the app will be available here :
https://georgetown-analytics.github.io/Air-Pollution/app/test

A copy avaible and running here:
https://collaer.github.io/simplemap/Air-Pollution/app/
