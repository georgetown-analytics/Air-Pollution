from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

class GroundStation(db.Model):
    __tablename__ = "ground_station"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), unique=False, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    measures = db.relationship('Measure', backref='groundStation', lazy=True)


    def __init__(self, type, active, lat, lon):
        self.type = type
        self.active = active
        self.lat = lat
        self.lon = lon

class Measure(db.Model):
    __tablename__ = "measure"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), unique=False, nullable=False)
    value = db.Column(db.Float, unique=False, nullable=False)
    time = db.Column(db.String(37), default=True, nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('ground_station.id'))
    #note; Must use the __tablename__ string to set foreign key

    def __init__(self, type, value, time, station_id):
        self.type = type
        self.value = value
        self.time = time
        self.station_id = station_id


@app.route("/")
def hello_world():
    return jsonify(hello="Ground stations in db")
