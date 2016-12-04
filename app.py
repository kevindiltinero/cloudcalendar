
###################################            LOAD MODULES DATABASES AND CLASSIFIER             ###############################
from flask import Flask,url_for, render_template, request
import sqlite3
import json

###################################        PYTHON FUNCTIONS         ##################################


def event_writting(id, title, start, end, category):
    #Set up the connection.
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    #Consolidate into an array
    theevent = [id, title, start, end, category]
    # Write ABT into the Database
    c.execute('INSERT INTO calendarevents (id, title, start, end, category)'\
              'VALUES (?, ?, ?, ?, ?)', theevent)
    conn.commit()


def database_to_json():
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    command = "SELECT * FROM calendarevents"
    c.execute(command)
    results = c.fetchall()
    eventrows = []
    category_color_mapping = {
        'Algorithms': 'red',
        'Java': 'green',
        'Programming': 'blue',
        'CloudComputing': 'purple',
        'DataScience': 'brown',
        'DataVisualisation': 'orange'}
    for row in results:
        eventrows.append({'id':row[0], 'title':row[1], 'start':row[2], 'end':row[3], 'color':category_color_mapping[row[4]]})
    jsonobject = {'glossary':eventrows}
    with open('static/random.json', "w") as outfile:
        json.dump(jsonobject, outfile, indent=4)


def updateevent(eventid, eventtitle, eventcategory):
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    # command = 'UPDATE calendarevents SET title = '+'"Rojer"'+' WHERE id = '+str(eventid)+';'
    command = "UPDATE calendarevents SET title = '"+eventtitle+"' WHERE id = "+str(eventid)+";"
    c.execute(command)
    conn.commit()
    command = "UPDATE calendarevents SET category = '"+eventcategory+"' WHERE id = "+str(eventid)+";"
    c.execute(command)
    conn.commit()


def updatedate(eventid, eventstart):
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    # command = 'UPDATE calendarevents SET title = '+'"Rojer"'+' WHERE id = '+str(eventid)+';'
    command = "UPDATE calendarevents SET start = '"+eventstart+"' WHERE id = "+str(eventid)+";"
    c.execute(command)
    conn.commit()


def grab_single_event(eventtitle):
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    command = "SELECT * FROM calendarevents WHERE title = "+eventtitle+"; "
    c.execute(command)
    results = c.fetchall()
    event = results[0]


def remove_event(eventid):
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    command = "DELETE FROM calendarevents WHERE ID ="+str(eventid)+";"
    c.execute(command)
    conn.commit()


##########################    INSTANTIATE THE FLASK APP  ##################################
app = Flask(__name__)



# ##########################                MAIN PAGE               ##################################
@app.route('/', methods=['GET', 'POST'])
def index():
    database_to_json()

    # If the form was used get the day and hour and do the above prediction with that day and hour
    if request.method == 'POST':
        #GET ALL VALUES FROM AJAX
        title = request.json['title']
        category = request.json['categor']
        eventstart = request.json['start']
        eventend = request.json['start']
        eventid = request.json['eventid']
        print(title, category, eventstart, eventend, eventid)

        #WRITE INTO THE DATABASE
        event_writting(eventid, title, eventstart, eventend, category)
        database_to_json()
        # Send over the events and the predictions results over to the main page to plot colors and icons.
        return render_template('index.html')
    database_to_json()
    return render_template('index.html')
#
#
#
# ########################## EVENTS PAGE  ##################################
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
        updateevent(eventid, newtitle, newcategory)

        # Send over the events and the predictions results over to the main page to plot colors and icons.
        return render_template('index.html')
    # database_to_json()
    return render_template('index.html')
#
#
#
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
#
#
#
@app.route('/drag', methods=['POST', 'GET'])
def drag():
    # If the form was used get the day and hour and do the above prediction with that day and hour
    if request.method == 'POST':
        eventid = request.json['eventid']
        eventstart = request.json['eventstart']
        print(eventid, eventstart)
        updatedate(eventid, eventstart)

        # Send over the events and the predictions results over to the main page to plot colors and icons.
        return render_template('index.html')
    # database_to_json()
    return render_template('index.html')
#
#
#
#
@app.route('/remove', methods=['POST', 'GET'])
def remove():
    # If the form was used get the day and hour and do the above prediction with that day and hour
    if request.method == 'POST':
        eventid = request.json['eventid']
        print(eventid)
        remove_event(eventid)
        # updatedate(eventid, eventstart)

        # Send over the events and the predictions results over to the main page to plot colors and icons.
        return render_template('index.html')
    # database_to_json()
    return render_template('index.html')
#




if __name__ == '__main__':
    app.run(debug=True)