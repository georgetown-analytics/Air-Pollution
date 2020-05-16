# Standard modules
import numpy as np
import random
import pandas as pd
from flask import Flask, request, render_template

# Scikit Learn modules
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.metrics import f1_score
from sklearn.compose import ColumnTransformer

model = None
app = Flask(__name__)

# Load index page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def get_prediction():
    ####################################
    # Load Data
    ####################################
    url = 'https://gt-airpollution-machinelearning-data.s3.us-east-2.amazonaws.com/eda.csv'
    df = pd.read_csv(filepath_or_buffer=url, sep=",", encoding="utf-8", header=0)
    data = df[['x', 'y', 'dayofweek', 'sin_day', 'cos_day', 'sin_year', 'cos_year', 'TEMP', 'cos_wind', 'sin_wind',
               'Wind-Rate', 'DEW', 'SKY', 'VIS', 'ATM']]

    ####################################
    # User Input
    ####################################
    station = request.args.get('station_id')

    if station == 'Arlington':
        x = 38.900099
        y = 77.081078
    elif station == 'Courthouse':
        x = 38.88812
        y = -77.088094
    elif station == 'McMillan 1':
        x = 38.92185
        y = -77.013271
    elif station == 'V Street':
        x = 38.918491
        y = -77.037393

    temperature = float(request.args.get('temp'))
    dewp = float(request.args.get('dewp'))

    ####################################
    # Random Forest
    ####################################

    # set samples matrix [n_samples, n_features] (X) and target (y)
    features = df[[
        'x',
        'y',
        'dayofweek',
        'sin_day',
        'cos_day',
        'sin_year',
        'cos_year',
        'TEMP',
        'cos_wind',
        'sin_wind',
        'Wind-Rate',
        'DEW',
        'SKY',
        'VIS',
        'ATM'
    ]].astype(np.float64)

    features.loc[:, 'dayofweek'] = features['dayofweek'].astype('category')

    numericColumns = ['x', 'y',
                      'dayofweek', 'sin_day', 'cos_day', 'sin_year', 'cos_year',
                      'TEMP', 'cos_wind', 'sin_wind', 'Wind-Rate', 'DEW', 'SKY', 'VIS', 'ATM'
                      ]
    categoricalColumns = ['dayofweek']

    gs = df[['station_id']]

    labels = df[[
        'pm25',
        'AQI_VALUE',  # pm25 transformed using EPA methodology
        'AQI_class'  # pm25 transformed into EPA categorical class
    ]]

    labels.loc[:, "polluted"] = (labels.loc[:, "AQI_class"] != "Good")

    y = labels["polluted"]
    X = features

    # fit data to model
    y_train = labels["polluted"]
    X_train = features

    # Create randomforest object
    forest = RandomForestClassifier(random_state=91)

    # Train the model using the training sets
    forest.fit(X_train, y_train)

    # Make predictions using the user input
    y_prediction = forest.predict(
        [[
            x,
            y,
            3,
            -1.100051e-02,
            1.275056e-02,
            -0.126217,
            -0.039860,
            temperature, 
            -3.994828e-02,
          -1.963345e-02,
            4.376273,
            dewp,
            33870.176884,
            15478.080912,
            1805.021227]]
        )

    ####################################
    # Generate HTML Page
    ####################################

    return render_template('prediction.html', station=station, x=x, y=y, temperature=temperature,
                           prediction=y_prediction)

# Run app
if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=80)