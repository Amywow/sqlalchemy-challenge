import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
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
        f"/api/v1.0/startdate(YYYY-mm-dd)<br/>"
        f"/api/v1.0/startdate/enddate(YYYY-mm-dd)<br/>"
    )

# Define routes
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    """Returns the date as the key and the value as the precipitation for last year"""
    # Calculate the date one year from the last date in data set.
    last_year = dt.date(2017, 8, 23)-dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    last_years = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_year).all()
    
    # Insert value for key and value
    prev_year = [{date: value} for date, value in last_years]
    
    # Close the session
    session.close()
    return jsonify(prev_year)

# Define routes
@app.route("/api/v1.0/stations")
def stations():

    """Return a list of station names"""
    # Query all passengers
    names = session.query(measurement.station).group_by(measurement.station).all()
    station_name = [item[0] for item in names]

    # Close the session
    session.close()
    
    return jsonify(station_name)

# Define routes
@app.route("/api/v1.0/tobs")
def tobs():
    
    """Return dates and temperature observation of USC0051928 for the last 12 months"""
    # Perform a query to retrieve the data for the last 12 months of dates and temperature observation with the most active station id
    last_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    temperature_last = session.query(measurement.date, measurement.tobs).filter((measurement.station == 'USC00519281')&(measurement.date >= last_year)).all()
    temp_prev = [{date: temp} for date, temp in temperature_last]
    
    # Close the session
    session.close()
    
    return jsonify(temp_prev)
    

# Define routes
@app.route("/api/v1.0/<start>")
def startdate(start):
    # Create a list 
    start_result = []
    
    # Convert the input to correct format
    start_time = dt.datetime.strptime(start, "%Y-%m-%d")
    
    # Query minimum, maximum and averge for certain period
    temp_start = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start_time).all()
    
    # Insert data to the list
    for value in temp_start:
        start_result.append(value)
    start_r = list(start_result[0])
    
    # Close the session
    session.close()
    
    return jsonify(start_r)
        
# Define routes
@app.route("/api/v1.0/<start>/<end>")
def period(start,end):
    # Create a list 
    result = []
    
    # Convert the input to correct format
    start_time = dt.datetime.strptime(start, "%Y-%m-%d")
    end_time = dt.datetime.strptime(end, "%Y-%m-%d")
    
    # Query minimum, maximum and averge for certain period
    temp_part = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter((measurement.date >= start_time)&(measurement.date <= end_time)).all()
    
    # Insert data to the list
    for value in temp_part:
        result.append(value)
    period_r = list(result[0])
    
    # Close the session
    session.close()
    return jsonify(period_r)    


# Define main behaviour
if __name__ == '__main__':
    app.run(debug=True)
