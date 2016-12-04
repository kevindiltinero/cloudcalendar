
###################################            LOAD MODULES DATABASES AND CLASSIFIER             ###############################
from flask import Flask,url_for, render_template, request
from wtforms import Form, SelectField, StringField, BooleanField, TextAreaField, validators
import pickle
import sqlite3
import datetime
from datetime import date
import calendar
import json

###################################        PYTHON FUNCTIONS         ##################################

# TIME CHECKER
# This uses the datetime module to get the current day and hour
def check_time():
    #Get the current hour and date
    time = str(datetime.datetime.now())
    hour = time[11:13]
    my_date = date.today()
    day = calendar.day_name[my_date.weekday()]
    return [day, hour]


# MATRIX GENERATOR FOR THE CLASSIFIER
# This function creates the matrix(nested list) that the classifier will predict like so:
# day/time from checktime() are it's parameters, selects every row from ABT with that time/day,
# The values within the row are excluded unless they correspond to our descriptive features the model expects
# ULTIMATELY- Outputs nested list for our classifier
def select_from():
    #MAPPING IT
    daymapping = {'Monday': '0', 'Tuesday': '1', 'Wednesday':'2', 'Thursday':'3', 'Friday': '4'}
    hourmapping = {'09': '0', '10': '1', '11': '2', '12': '3', '13': '4', '14':'5'}

    conn = sqlite3.connect('occupancy.db')
    c = conn.cursor()
    c.execute("SELECT Room, Type, Associated "
              "FROM first_abt "
              "WHERE theDate = 0 AND Time = 1 ")

    results = c.fetchall()
    matrix = []

    for result in results:
        matrix.append(list(result))

    return matrix


def event_writting(id, title, start, end):
    #Set up the connection.
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    #Consolidate into an array
    theevent = [id, title, start, end]
    # Write ABT into the Database
    c.execute('INSERT INTO calendarevents (id, title, start, end)'\
              'VALUES (?, ?, ?, ?)', theevent)
    conn.commit()

# WRITING EVENTS
# Simple function to write events into the events table, isolated table just pertaining to events
def war_writting(day, hour, room, event, description):
    #Set up the connection.
    conn = sqlite3.connect('occupancy.db')
    c = conn.cursor()
    #Consolidate into an array
    theevent = [day, hour, room, event, description]
    # Write ABT into the Database
    c.execute('INSERT INTO eventsx (datey, hour, room, event, description)'\
              'VALUES (?, ?, ?, ?, ?)', theevent)
    conn.commit()


# WARCHECKING   Checking Events.
# This checks if there is any events that need to be plotted with the icons
# It checks it by seing if day and time match the current day time
def war_checking(day, hour):
        eventpicture_mapping = {'study': 'meet.jpg', 'talk': 'speech.jpg', 'cancel': 'cancel.jpg',
                                'exam': 'exam.jpg'}
        eventicon_mapping = {'study': 'meet2.png', 'talk': 'career.png', 'cancel': 'cancelled.png',
                             'exam': 'exam.png'}
        # Change the rooms to slices when sending the info back.



def database_to_json():
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    command = "SELECT * FROM calendarevents"
    c.execute(command)
    results = c.fetchall()
    eventrows = []
    category_color_mapping = {'work': 'red', 'entertainment': 'green'}
    for row in results:
        eventrows.append({'id':row[0], 'title':row[1], 'start':row[2], 'end':row[3], 'color':category_color_mapping[row[4]]})
    jsonobject = {'glossary':eventrows}
    with open('static/random.json', "w") as outfile:
        json.dump(jsonobject, outfile, indent=4)

def updateevent(eventid):
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    command = 'UPDATE calendarevents SET title = "Rojer" WHERE id = '+str(eventid)+';'
    c.execute(command)
    conn.commit()

def grab_single_event(eventtitle):
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    command = "SELECT * FROM calendarevents WHERE title = "+eventtitle+"; "
    c.execute(command)
    results = c.fetchall()
    event = results[0]




##########################    INSTANTIATE THE FLASK APP  ##################################
app = Flask(__name__)


##########################                MAIN PAGE               ##################################
@app.route('/home', methods=['GET', 'POST'])
def index():
    database_to_json()

    # If the form was used get the day and hour and do the above prediction with that day and hour
    if request.method == 'POST':
        title = request.json['title']
        other = request.json['start']
        testing = "hello"
        print(title, other)
        event_writting(1, title, other, other)
        database_to_json()
        # Send over the events and the predictions results over to the main page to plot colors and icons.
        return render_template('index.html')
    database_to_json()
    return render_template('index.html')


########################## EVENTS PAGE  ##################################


@app.route('/events', methods=['POST', 'GET'])
#This is simply the rendering of the page from the navigation bar. See form functionality below.
def events():
    # If the form was used get the day and hour and do the above prediction with that day and hour
    if request.method == 'POST':
        newtitle = request.json['newtitle']
        newcategory = request.json['newcategory']
        oldstart = request.json['oldstart']
        oldtitle = request.json['oldtitle']
        eventid = request.json['eventid']
        print(newtitle, newcategory, oldstart, oldtitle)
        updateevent(eventid)

        # Send over the events and the predictions results over to the main page to plot colors and icons.
        return render_template('index.html')
    # database_to_json()
    return render_template('index.html')

@app.route('/query', methods=['POST', 'GET'])
#This is simply the rendering of the page from the navigation bar. See form functionality below.
def query():
    # If the form was used get the day and hour and do the above prediction with that day and hour
    if request.method == 'POST':
        queryevent = request.json['queryevent']
        print(queryevent)

        # Send over the events and the predictions results over to the main page to plot colors and icons.
        return render_template('index.html')
    # database_to_json()
    return render_template('index.html')

################################           EVENT FORM FUNCTION            #####################################

# EVENTS FORM
# # Gets the data that they input into the events form and writes it into the events table
# @app.route('/hello', methods=['POST'])
# def hello():
#     form = HelloForm(request.form)
#     if request.method == 'POST':
#         event = request.form['event']
#         day = request.form['sayhello']
#         hour = request.form['saygoodbye']
#         room = request.form['slice']
#         descr = request.form['description']
#         war_writting(day, hour, room, event, descr)
#         return render_template('events.html', form=form)

# @app.route('/updaterecord', methods=['POST'])
# def update_record():
#     # If the form was used get the day and hour and do the above prediction with that day and hour
#     if request.method == 'POST':
#         nwtitle = request.json['newtitle']
#         ldtitle = request.json['oldtitle']
#         ldstart = request.json['oldstart']
#
#
#         event_writting(1, title, other, other)
#         database_to_json()
#         # Send over the events and the predictions results over to the main page to plot colors and icons.
#         return render_template('index.html', form=form)
#     database_to_json()
#     return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
