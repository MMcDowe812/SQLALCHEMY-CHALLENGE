# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine=create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measure = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation"""
    # Query list of precipitation
    year_ago = dt.date(2017,8,23)-dt.timedelta(days=365)

    results=session.query(measure.date, measure.prcp).filter(measure.date >= year_ago).all()
    session.close()
    # precip = {date: prcp for date, prcp in precipitation}

    precip=[]
    for date, prcp in results:
        precip_dict={}
        precip_dict["Date"]=date
        precip_dict["Precipitation"]=prcp
        precip.append[precip_dict]


    return jsonify(precip)

    #getting stations
@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)

    results = session.query(station.station).all()
    session.close()
    
    station = list(np.ravel(results))
    return jsonify(stations=stations)


# finding temperatures
@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    year_ago = dt.date(2017,8,23)-dt.timedelta(days=365)

    results_temps = session.query(measure.tobs).filter(measure.date >= year_ago).filter(measure.station=='USC00519281').all()
    session.close()

    temps = list(np.ravel(results_temps))
    
    return jsonify(temps  = temps)

# @app.route("api/v1.0/start")
# def start():


if __name__ == '__main__':
    app.run(debug=True)