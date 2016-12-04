import sqlite3

def calendartable():
    #Set up the connection to the database and the cursor
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()

    #Creating the table for the ABT
    c.execute('CREATE TABLE IF NOT EXISTS calendarevents (id INT, title TEXT, start TEXT, end TEXT)')

    # # Write ABT into the Database
    # c.executemany('INSERT INTO first_abt (theDate, Day, Time, Module, Room, Capacity, Type, Registered, Over3,'\
    #           'Authenticated, Associated, TARGET) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', csv)
    # conn.commit()

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


def events():
    #Set up the connection to the database and the cursor
    conn = sqlite3.connect('occupancy.db')
    c = conn.cursor()

    #Creating the table for the ABT
    c.execute('CREATE TABLE IF NOT EXISTS eventsx'\
              ' (Datey TEXT, Hour TEXT, Room TEXT, Event TEXT, description TEXT)')


def delete_relevent():
    #Set up the connection to the database and the cursor
    conn = sqlite3.connect('occupancy.db')
    c = conn.cursor()

    #Reset
    c.execute("DELETE FROM eventsx;")

#abt()

#events()

# calendartable()
# event_writting(9, 'paulsimon', '2016-11-29T12:30:00', '2016-11-3T12:40:00')

# conn = sqlite3.connect('calendar.db')
# c = conn.cursor()
# c.execute('ALTER TABLE calendarevents ADD COLUMN category string;')


