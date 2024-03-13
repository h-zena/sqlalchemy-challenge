# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Welcome to the Climate App!<br/><br/>"
        f"Available routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a>: Precipitation data for the last 12 months<br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a>: List of weather stations<br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a>: Temperature observations for the most active station in the last year<br/>"
        f"/api/v1.0/&lt;start&gt;: Temperature statistics (min, avg, max) for a given start date (format: YYYY-MM-DD)<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;: Temperature statistics (min, avg, max) for a given start-end date range (format: YYYY-MM-DD/YYYY-MM-DD)"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)

    results=session.query(measurement.date, measurement.prcp).filter(measurement.date>="2016-08-23").all()

    return {d:p for d,p in results}


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.id,Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
    session.close()
    all_station=[]
    for id,station,name,latitude,longitude,elevation in results:
        station_dict={}
        station_dict['Id']=id
        station_dict['station']=station
        station_dict['name']=name
        station_dict['latitude']=latitude
        station_dict['longitude']=longitude
        station_dict['elevation']=elevation
        all_station.append(station_dict)
    return jsonify(all_station)

@app.route('/api/v1.0/tobs')
def station():
    session=Session(engine)
    results=session.query( measurement.date, measurement.tobs).filter((measurement.date>="2016-08-23")&(measurement.station=="USC00519281")).all()
    return {t:s for t,s in results}

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def date_range(start,end='2017-08-23'):
    session=Session(engine)
    join=session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).filter((measurement.date>=start)&(measurement.date<=end)).first()

    print("data:",join)
    return {"min":join[0],"avg":join[1],"max": join[2]}

if __name__ == '__main__':
    app.run(debug=True)