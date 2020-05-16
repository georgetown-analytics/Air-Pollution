# Standard modules
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import Flask, request, render_template

# Scikit Learn modules
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge

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

    temperature = request.args.get('temp')
    dewp = request.args.get('dewp')


    ####################################
    # Linear Regression
    ####################################
    # set samples matrix [n_samples, n_features] (X) and target (y)
    features = ['x', 'y', 'dayofweek', 'sin_day', 'cos_day', 'sin_year', 'cos_year', 'TEMP', 'cos_wind', 'sin_wind',
                'Wind-Rate', 'DEW', 'SKY', 'VIS', 'ATM']
    target = ['pm25']

    # fit data to model
    X_train = df[features]
    y_train = df[target]

    # Create linear regression object
    lr = LinearRegression()

    # Train the model using the training sets
    lr.fit(X_train, y_train)

    # User input
    userinput = [[x, y, 3, -1.100051e-02, 1.275056e-02, -0.126217, -0.039860, temperature, -3.994828e-02,
                  -1.963345e-02, 4.376273, dewp, 33870.176884, 15478.080912, 1805.021227]]

    X_test = pd.DataFrame(userinput, columns=['x', 'y', 'dayofweek', 'sin_day', 'cos_day', 'sin_year', 'cos_year', 'TEMP', 'cos_wind', 'sin_wind',
                'Wind-Rate', 'DEW', 'SKY', 'VIS', 'ATM'])

    # Make predictions using the user input
    y_prediction = lr.predict(X_test)

    ####################################
    # Generate HTML Page
    ####################################

    return render_template('prediction.html', station=station, x=x, y=y, temperature=temperature,
                           prediction=y_prediction)


# Run app
if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=80)