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

@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)

    #Date data 
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    one_year_ago = (dt.datetime.strptime(last_date[0],'%Y-%m-%d') \
                - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    
    #Dates and Temps
    results = session.query(measurement.date,measurement.tobs).\
            filter(measurement.date >= one_year_ago).\
            order_by(measurement.date).all()
    
    #Jsonify/Dictionairy clean up 
    results_tobs = []

    for date,tobs in results: 
        new_dict = {}
        new_dict[date] = tobs
        results_tobs.append(new_dict)
    
    session.close()

    return jsonify(results_tobs)

@app.route("/api/v1.0/<start>")
def temp_range_start(start): 
    
    session = Session(engine)
    
    temp_list = []
    #define any start date in '%Y-%m-%d'
    results = session.query(measurement.date,func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).\
    filter(measurement.date >= '2010-01-01').group_by(measurement.date).all()
    
    for date, min, avg, max in results:
        new_dict = {}
        new_dict["Date"] = date
        new_dict["TMIN"] = min
        new_dict["TAVG"] = avg
        new_dict["TMAX"] = max
        temp_list.append(new_dict)

    session.close() 
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>/<end>")
def temp_range_start_end(start,end):

    session = Session(engine)

    temp_list = []
 #Pick a start and end date for the data to query and pull
    results = session.query( measurement.date,func.min(measurement.tobs),func.avg(measurement.tobs),\
                            func.max(measurement.tobs)).\
                        filter(and_(measurement.date >= '2010-01-01', measurement.date <= '2010-12-31')).\
                            group_by(measurement.date).all()
    
    for date,min,avg,max in results:
        new_dict = {}
        new_dict["Date"] = date
        new_dict["TMIN"] = min
        new_dict["TAVG"] = avg
        new_dict["TMAX"] = max
        temp_list.append(new_dict)
    
    session.close()
    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)