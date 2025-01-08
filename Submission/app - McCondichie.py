# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################


## 1. Welcome page
##Added breaks and context for readability and hoping to make the urls for dates more user friendly

@app.route('/')
def welcome():
    return(
        f"Available routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/<start><br/>"
            f"(Enter a date to the end of the url above to see results from a specific start date.)<br/>"
            f"<br/>"
        f"/api/v1.0/<start>/<end><br/>"
            f"(Enter a start date, followed by ' / ', then an end date<br/>" 
            f"to the above url to see results for a date range.)"
    )


## 2. Precipitation for the last 12 months of data 

@app.route("/api/v1.0/precipitation")
def year_precipitation():
    session = Session(engine)

    rows = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").all()

    session.close()

    prcp_dict = []
    for row in rows:
        prcp_dict.append({row[0] : row[1]})

    return jsonify(prcp_dict)



## 3. List of all stations in the data 

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    rows = session.query(Station.station, Station.name).all()

    session.close()

    station_dict = []
    for row in rows:
        station_dict.append({'Station' : row[0], 'Name' : row[1]})

    return jsonify(station_dict)


## 4. Temp data for most active station in data
##I know from part 1 that the most active station is USC00519281

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    rows = session.query(Measurement.tobs, Measurement.date, Measurement.station).filter(Measurement.date >= "2016-08-23", Measurement.station == "USC00519281").all()

    tobs_dict = []
    for row in rows:
        tobs_dict.append({'Temperature' : row[0], 'Date' : row[1], 'Station' : row[2]})

    session.close()

    return jsonify(tobs_dict)


## 5a. Temp data for a given start date

@app.route("/api/v1.0/<start>")
def start_stats(start):
    session = Session(engine)

    rows = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    start_dict = []
    for row in rows:
        start_dict.append({'Date' : row[0], 'Min Temp' : row[1], 'Max Temp' : row[2], 'Avg Temp' : row[3]})

    session.close()

    return jsonify(start_dict)


## 5b. Temp data for a given date range

@app.route("/api/v1.0/<start>/<end>")
def date_range(start, end):
    session = Session(engine)

    rows = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date < end).all()

    range_dict = []
    for row in rows:
        range_dict.append({'Start Date' : start, 'End Date' : end,  'Min Temp' : row[1], 'Max Temp' : row[2], 'Avg Temp' : row[3]})

    session.close()

    return jsonify(range_dict)



if __name__ == '__main__':
    app.run(debug=True)