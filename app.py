#dependancies for date ,pandas and numpy
import datetime as dt 
import pandas as pd 
import numpy as np 

#dependancies for database setup
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask , jsonify

######################################################################
####                      Setup the database                    ######
######################################################################
#assume sqlite database for hawaii weather 
#is saved in same location as the app code. if it is different location then setup the path accordingly using
#forward slash 
#Valid SQLite URL forms are:
#sqlite:///:memory: (or, sqlite://)
#sqlite:///relative/path/to/file.db
#sqlite:////absolute/path/to/file.db

engine = create_engine('sqlite:///hawaii.sqlite' , connect_args={'check_same_thread': False})
#reflect the database into ORM
Base = automap_base()
Base.prepare(engine, reflect = True)
#Reflect tables from the database into their own classes using ORM .  Note that we arelady know the tables
#if we don't know the table names then use Base.classes.keys() to get the tables
#Variable name start with upper case donat an instance of a class 
Measurement = Base.classes.measurement
Station = Base.classes.station
##Create session to link python to the database 
session = Session(engine)

########################################################################
#####                    SETUP FLAS for web app                 ########
########################################################################
app = Flask(__name__)
###create root welcome page
@app.route('/')
def welcome():
    return(
        ''' <br/>
        Welcome to the Climate Analysis API! <br/>
        Availble routes: <br/>
        /api/v1.0/percipitation <br/>
        /api/v1.0/stations <br/>
        /api/v1.0/tobs <br/>
        /api/v1.0/temp/start/end <br/>
        '''
    )

# Percipitation route that shows percipitation by date
@app.route('/api/v1.0/percipitation')
def percipitation():
    #previous year for maximum date in the data which Aug 23 2017
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #query database to get percipation by date.
    percipitation = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= prev_year).all()
    #create dictionary from query result
    percip = {date: prcp for date, prcp in percipitation}
    #retunr dictionary as json
    return jsonify(percip)

#Define station route where all stations will be displayed
@app.route('/api/v1.0/stations')
def stations():
    #Get all the station list from station
    results = session.query(Station.station).all()
    # as the qyert output is single column, lets convert this into signle dimension array using no.ravel()
    # remeber the query retsuls are tuples 
    stations  = list(np.ravel(results))
    return jsonify( stations = stations)

## temparture observations route for temperature from previous year using max date from the data
@app.route('/api/v1.0/tobs')
def temp_monthly():
    #calcualte the date one year ago using max date of Aug 23 2017
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #now query the temprature obs for stations that has most observarion. based on previous analysis
    #station USC00519281 has the most temperature observations
    results = session.query (Measurement.tobs).\
             filter(Measurement.station == 'USC00519281').\
              filter (Measurement.date >= prev_year) .all()
    # now as the result is single column in the form of tuple convert it to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#Route to provide temparature stats for a start and end date
@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')

# define stats function run for above mentioned routes. the function takes in two parameters
def stats(start = None , end = None):
    #query to get stats
    sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results =  Session.query (*sel).\
                  filter(Measurement.date >= start).\
                  filter(Measurement.date <= end ).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__ == "__main__":
    app.run(debug=True)

#app = Flask(__name__)
##define root route
#@app.route('/')
##function that will go into the rout
#def hello_world():
#    return "Hello World"
##Skill drill Think of some simple route and then try to reate the route and implement the logic
#@app.route('/my_test')
#def my_logic():
#    message =  f"This is my testing route.<br/>"\
#          f"Try printing different lines"
#    return message