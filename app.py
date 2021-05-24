import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False})


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
session= Session(engine)
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
        f"/api/v1.0/(start)<br/>"
        f"/api/v1.0/(start)/(end)"
    )

@app.route("/api/v1.0/precipitation")
def Precipitation():
    recent_year=dt.date(2017, 8, 23) - dt.timedelta(days=366)
    print('Query Date:', recent_year)

    year_prec=(session.query(Measurement.date,func.max(Measurement.prcp))
        .filter(func.strftime('%Y-%m-%d',Measurement.date) > recent_year)
        .group_by(Measurement.date)
        .all())
    result= list(np.ravel(year_prec))
    return jsonify(result)
        
   

@app.route("/api/v1.0/stations")
def Stations():
    year_prec=(session.query(Station.station)
        .all())
    result= list(np.ravel(year_prec))
    return jsonify(result)

@app.route("/api/v1.0/tobs")
def tobs():
    recent_year=dt.date(2017, 8, 23) - dt.timedelta(days=366)
    year_prec=(session.query(Measurement.tobs)
        .filter(Measurement.station=='USC00519281')
        .filter(Measurement.date>recent_year)
        .all())
    result= list(np.ravel(year_prec))
    return jsonify(result)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def averages(start=None, end=None):
    if not end: 
        query=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)
        ).filter(Measurement.date>start).all()
        result= list(np.ravel(query))
        return jsonify(result)

    query=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)
    ).filter(Measurement.date>start).filter(Measurement.date<end).all()
    result= list(np.ravel(query))
    return jsonify(result)
    



if __name__ == '__main__':
    app.run(debug=True)
