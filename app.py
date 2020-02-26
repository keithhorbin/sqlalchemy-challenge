# imports
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

# db engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

# Reflect Database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# assign measurement/station classes to its var Measurement/Station
Measurement = Base.classes.measurement
Station = Base.classes.station

# create session
session = Session(engine)

# Flask
app = Flask(__name__)

# app routes
app.config["JSON_SORT_KEYS"] = False

#home base
@app.route("/")
def index():
    return (
        f"Available Routes:<br>"
        f"                 <br>"
        f"Precipitation for last year: /api/v1.0/precipitation<br/>"
        f"List of all stations: /api/v1.0/stations<br/>"
        f"Date and temperature observations from the last year: /api/v1.0/tobs<br/>"        
        f"Min, Avg, Max Temp given a start date up to most current date in db: /api/v1.0/2015-12-31<br/>"
        f"Min, Avg, Max Temp given a start and end date: /api/v1.0/2016-12-17/2016-12-30<br/>"
    )

# Convert the query results to a Dictionary using `date` as the key and `prcp` as the value. Return the JSON representation of your dictionary.    
@app.route("/api/v1.0/precipitation")    
def precip():
    results = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= '2016-08-23')\
    .filter(Measurement.date <= '2017-08-23')\
    .order_by(Measurement.date)
    
    precip_data = []
    for result in results:
        precip_dict = {}
        precip_dict['date'] = result.date
        precip_dict['prcp'] = result.prcp
        precip_data.append(precip_dict)

    return jsonify(precip_data)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    #query for the data, practicing join even though station table has both columns queried below
    results = session.query(Station.name, Measurement.station)\
    .filter(Station.station == Measurement.station)\
    .group_by(Station.name).all()

    stations_data = []
    for result in results:
        stations_dict = {}
        stations_dict['name']    = result.name
        stations_dict['station'] = result.station
        stations_data.append(stations_dict)
    
    return jsonify(stations_data)

# Query for the dates and temperature observations from a year from the last data point. Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.date >= '2016-08-23')\
    .filter(Measurement.date <= '2017-08-23')\
    .order_by(Measurement.date)

    tobs_data = []
    for result in results:
        tobs_dict = {}
        tobs_dict['date'] = result.date
        tobs_dict['tobs'] = result.tobs
        tobs_data.append(tobs_dict)
    
    return jsonify(tobs_data)

# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def temp_stats_start(start):

    results = session.query\
    (func.min(Measurement.tobs).label('min'),\
    func.avg(Measurement.tobs).label('avg'),\
    func.max(Measurement.tobs).label('max'))\
    .filter(Measurement.date >= start).all()
    
    start_stats_data = []
    for result in results:
        start_stats_dict = {}
        start_stats_dict['Start Date'] = start
        start_stats_dict['Min Temp'] = result.min
        start_stats_dict['Avg Temp'] = result.avg
        start_stats_dict['Max Temp'] = result.max
        start_stats_data.append(start_stats_dict)
    
    return jsonify(start_stats_data)

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def temp_stats_start_end(start, end):

    results = session.query(func.min(Measurement.tobs).label('min'),\
    func.avg(Measurement.tobs).label('avg'),\
    func.max(Measurement.tobs).label('max'))\
    .filter(Measurement.date >= start)\
    .filter(Measurement.date <= end).all()

    start_end_stats_data = []
    for result in results:
        start_end_stats_dict = {}
        start_end_stats_dict['Start Date'] = start
        start_end_stats_dict['End Date'] = end
        start_end_stats_dict['Min Temp'] = result.min
        start_end_stats_dict['Avg Temp'] = result.avg
        start_end_stats_dict['Max Temp'] = result.max
        start_end_stats_data.append(start_end_stats_dict)
    
    return jsonify(start_end_stats_data)

if __name__ == '__main__':
    app.run(debug=True)
