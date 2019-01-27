#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil import parser
import pygal

from database import DB_CURSOR

# Set time period that will be analyzed
analyzed_period_start = '1.3.2019'
analyzed_period_finish = '31.10.2019'


def day_of_purchase_chart():
    DB_CURSOR.execute('SELECT ROUND(avg(flight_fare_flight_1), 2), ROUND(avg(flight_fare_flight_2), 2), '
                      'day_of_download FROM Flights GROUP BY day_of_download')

    rows = DB_CURSOR.fetchall()

    day_of_download = []
    flight_fare_flight_1 = []
    flight_fare_flight_2 = []

    for row in rows:
        flight_fare_flight_1.append(row[0])
        flight_fare_flight_2.append(row[1])
        day_of_download.append(row[2])

    bar_chart = pygal.Bar(title='Average price of flight ticket on certain purchase days (in CZK)',
                          print_values=True)
    bar_chart.add('First flight average price', flight_fare_flight_1)
    bar_chart.add('Second flight average price', flight_fare_flight_2)
    bar_chart.x_labels = day_of_download
    day_of_purchase_final_chart = bar_chart.render_to_file('bar_chart_day_of_purchase.svg')

    return day_of_purchase_final_chart


def day_of_departure_chart():
    DB_CURSOR.execute('SELECT ROUND(avg(flight_fare_flight_1), 2), ROUND(avg(flight_fare_flight_2), 2), '
                      'day_of_departure FROM Flights GROUP BY day_of_departure')

    rows = DB_CURSOR.fetchall()

    WEEKDAYS = {'po': 1, 'út': 2, 'st': 3, 'čt': 4, 'pá': 5, 'so': 6, 'ne': 7}
    rows.sort(key=lambda x: WEEKDAYS[x[2]])

    day_of_departure = []
    flight_fare_flight_1 = []
    flight_fare_flight_2 = []

    for row in rows:
        flight_fare_flight_1.append(row[0])
        flight_fare_flight_2.append(row[1])
        day_of_departure.append(row[2])

    bar_chart = pygal.Line(title='Average price of flight ticket for certain departure days (in CZK)',
                          print_values=True)
    bar_chart.add('First flight average price', flight_fare_flight_1)
    bar_chart.add('Second flight average price', flight_fare_flight_2)
    bar_chart.x_labels = day_of_departure
    day_of_departure_final_chart = bar_chart.render_to_file('bar_chart_day_of_departure_line.svg')

    return day_of_departure_final_chart


#def airlines_price_correlation_chart():
#price difference with departure date approaching
#prices of tickets changes for individual routes
#length of overstay correlation with whole price
#price + length of stay + probability of being late - vyhodnostni index
#convenient hours of arrival - most frequent hours of arrival (+vyhodnostni index)
#seats for lower price correlations (true or not, what change will come afterwards)

