import numpy as np  
import datetime as dt 
from sqlalchemy.ext.automap import automap_base 
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, func, and_
from flask import Flask, jsonify

#Db Set up 

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#DB reflection 
Base = automap_base()
#Table Reflect
Base.prepare(engine, reflect=True)

#Save reference
measurement = Base.classes.measurement
station = Base.classes.station

#Setup Flask 
app=Flask(__name__)

#Flask Routes

@app.route("/")
def welcome():
    """Listing availalble api routes."""
    return(
        f"API Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipiation():
    session = Session(engine)

    results = session.query(measurement.date, measurement.prcp).\
            order_by(measurement.date).all()
    
    prcp_dates = []

    for date,prcp in results:
        new_dict = {}
        new_dict[date] = prcp
        prcp_dates.append(new_dict)
    
    session.close()

    return jsonify(prcp_dates)

@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)

    stations = {}

    results = session.query(station.station, station.name).all()
    for s, name in results:
        stations[s] = name
    
    session.close()
    return jsonify(stations)


if __name__ == '__main__':
    app.run(debug=True)