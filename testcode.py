import sqlite3
import datetime
from datetime import date
import calendar
# Print predictions based on time
# Print the div styles based on time

#They choose a dropdown form date time
#Checks if that is taken
#Flask app checks time queries based on that
#Flask app checks if the divs need to be written to from the list




#Get the current hour and date
time = str(datetime.datetime.now())
hour = time[11:13]
my_date = date.today()
day = calendar.day_name[my_date.weekday()]

print(day, my_date)




# #Get the current hour and date
# conn = sqlite3.connect('occupancy.db')
# c = conn.cursor()
# c.execute("SELECT * FROM eventsx WHERE Datey = '07' AND Hour = '21'")
# results = c.fetchall()
# print(results)