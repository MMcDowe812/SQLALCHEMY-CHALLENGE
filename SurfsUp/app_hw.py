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
engine=create_engine("sqlite:///Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measure = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/temps/<start><br/>"
        f"/api/v1.0/temps/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    # session = Session(engine)

    """Return a list of precipitation"""
    # Query list of precipitation
    year_ago = dt.date(2017,8,23)-dt.timedelta(days=365)

    results=session.query(Measure.date, Measure.prcp).filter(Measure.date >= year_ago).all()
    session.close()
    precip = {date: prcp for date, prcp in results}

    # precip=[]
    # for date, prcp in results:
    #     precip_dict={}
    #     precip_dict["Date"]=date
    #     precip_dict["Precipitation"]=prcp
    #     precip.append[precip_dict]


    return jsonify(precip)

    #getting stations
@app.route("/api/v1.0/stations")
def stations():
    # session=Session(engine)

    results = session.query(Station.station).all()
    session.close()
    
    station = list(np.ravel(results))
    return jsonify(stations=station)


# finding temperatures
@app.route("/api/v1.0/tobs")
def tobs():
    # session=Session(engine)
    year_ago = dt.date(2017,8,23)-dt.timedelta(days=365)

    results_temps = session.query(Measure.tobs, Measure.station).filter(Measure.date >= year_ago).filter(Measure.station=='USC00519281').all()
    session.close()

    temps = list(np.ravel(results_temps))
    
    # for tob in temps:
    #     tobs_results.append[tob]
    
    return jsonify(temps=temps)

@app.route("/api/v1.0/temps/<start>")
@app.route("/api/v1.0/temps/<start>/<end>")
def date(start=None, end=None): 
    #return tmin, tmax, tavg

    SEL=[func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)]
    if not end:
        start = dt.datetime.strptime(start,"%m%d%Y")
        results = session.query(Measure.date,*SEL).filter(Measure.date >= start).all()
        
        session.close()
        Temps = list(np.ravel(results))
        return jsonify(Temps)
    
    # calculate for start and stop
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

    results_end = session.query(Measure.date, *SEL).filter(Measure.date >= start).filter(Measure.date <= end).all()

    session.close()

    temps = list(np.ravel(results_end))

    return jsonify (Temps=temps)

if __name__ == '__main__':
    app.run(debug=True)