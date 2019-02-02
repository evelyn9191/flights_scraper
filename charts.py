#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil import parser
import pygal

from database import DB_CURSOR

# Set time period that will be analyzed
ANALYZED_PERIOD_START = '15.03.2019'
ANALYZED_PERIOD_FINISH = '31.10.2019'
TIMESTAMP = datetime.now().strftime('%#d.%#m.%#Y')


def day_of_purchase_chart():
    """Chart about average prices of flight tickets based on weekday when they are bought."""
    DB_CURSOR.execute('SELECT ROUND(avg(flight_fare_flight_1), 2), '
                      'ROUND(avg(flight_fare_flight_2), 2), day_of_download '
                      'FROM Flights GROUP BY day_of_download')

    rows = DB_CURSOR.fetchall()

    day_of_download = []
    flight_fare_flight_1 = []
    flight_fare_flight_2 = []

    for row in rows:
        flight_fare_flight_1.append(row[0])
        flight_fare_flight_2.append(row[1])
        day_of_download.append(row[2])

    bar_chart = pygal.Bar(title='Average price of flight ticket '
                                'on certain purchase days (in CZK)',
                          print_values=True)
    bar_chart.add('First flight average price', flight_fare_flight_1)
    bar_chart.add('Second flight average price', flight_fare_flight_2)
    bar_chart.x_labels = day_of_download
    day_of_purchase_final_chart = bar_chart.render_to_file(
        f'bar_chart_day_of_purchase_{TIMESTAMP}.svg')

    return day_of_purchase_final_chart


def day_of_departure_chart():
    """Chart about average prices of flight tickets based on departure weekday."""
    DB_CURSOR.execute('SELECT ROUND(avg(flight_fare_flight_1), 2), '
                      'ROUND(avg(flight_fare_flight_2), 2), day_of_departure '
                      'FROM Flights GROUP BY day_of_departure')

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

    bar_chart = pygal.Line(title='Average price of flight ticket '
                                 'for certain departure days (in CZK)',
                          print_values=True)
    bar_chart.add('First flight average price', flight_fare_flight_1)
    bar_chart.add('Second flight average price', flight_fare_flight_2)
    bar_chart.x_labels = day_of_departure
    day_of_departure_final_chart = bar_chart.render_to_file(
        f'bar_chart_day_of_departure_line_{TIMESTAMP}.svg')

    return day_of_departure_final_chart


def airlines_avg_price_chart():
    """Chart about average prices of flight tickets based on airlines."""
    DB_CURSOR.execute('SELECT ROUND(avg(flight_fare_flight_1), 2), airlines_flight_1, '
                      'ROUND(avg(flight_fare_flight_2), 2), airlines_flight_2 '
                      'FROM Flights GROUP BY airlines_flight_1')
    rows = DB_CURSOR.fetchall()

    flight_fare_flight_1 = []
    flight_fare_flight_2 = []
    airlines_flight_1 = []
    airlines_flight_2 = []

    for row in rows:
        flight_fare_flight_1.append(row[0])
        airlines_flight_1.append(row[1])
        flight_fare_flight_2.append(row[2])
        airlines_flight_2.append(row[3])

    print(rows)

    bar_chart = pygal.Bar(title='Average price of flight ticket '
                                'based on airlines (in CZK)',
                          print_values=True)
    bar_chart.add('First flight average price', flight_fare_flight_1)
    bar_chart.add('Second flight average price', flight_fare_flight_2)
    bar_chart.x_labels = airlines_flight_1    # TODO: need to show both airlines_flight_x (merge it)
    airlines_avg_price_final_chart = bar_chart.render_to_file(
        f'bar_chart_airlines_avg_price_{TIMESTAMP}.svg')

    return airlines_avg_price_final_chart


def daily_price_chart():
    """Chart about average prices of flight tickets by date of departure."""
    arrival_destinations = ['FAO', 'KEF', 'NCE', 'TOS']
    departure_destinations = ['LIS']    # TODO: not working for LIS yet

    for destination in arrival_destinations:
        DB_CURSOR.execute("""SELECT ROUND(flight_fare, 2), date_of_departure '
                          'FROM Flights WHERE arrival_airport = ? AND date_of_departure 
                          BETWEEN '15.03.2019' AND '31.10.2019'""", (destination,))

        rows = DB_CURSOR.fetchall()
        print(rows)

        rows.sort(key=lambda x: datetime.strptime(x[1], '%d.%m.%Y'))

        flight_fare = []
        date_of_departure = []

        for row in rows:
            flight_fare.append(row[0])
            date_of_departure.append(row[1])

        bar_chart = pygal.Bar(title=f'Prices of flights PRG -> {destination} '
                                    f'by 27th January 2019 (in CZK)',
                              print_values=False)
        bar_chart.add('Flight fare', flight_fare)
        bar_chart.x_labels = date_of_departure
        bar_chart.render_to_file(f'bar_chart_daily_price_PRG_{destination}_{TIMESTAMP}.svg')

    for destination in departure_destinations:
        DB_CURSOR.execute("""SELECT ROUND(flight_fare, 2), date_of_departure '
                          'FROM Flights WHERE arrival_airport = ? AND date_of_departure 
                          BETWEEN '15.03.2019' AND '31.10.2019'""", (destination,))

        rows = DB_CURSOR.fetchall()
        print(rows)

        rows.sort(key=lambda x: datetime.strptime(x[1], '%d.%m.%Y'))

        flight_fare = []
        date_of_departure = []

        for row in rows:
            flight_fare.append(row[0])
            date_of_departure.append(row[1])

        bar_chart = pygal.Bar(title=f'Prices of flights {destination} -> PRG '
                                    f'by 27th January 2019 (in CZK)',
                              print_values=False)
        bar_chart.add('Flight fare', flight_fare)
        bar_chart.x_labels = date_of_departure
        bar_chart.render_to_file(f'bar_chart_daily_price_{destination}_PRG_{TIMESTAMP}.svg')


def price_by_hours_chart():
    """Chart about average prices of flight tickets based on daily time of departure."""
    # TODO: not working yet
    arrival_destinations = ['FAO', 'KEF', 'NCE', 'TOS']
    # departure_destinations = ['LIS']

    for destination in arrival_destinations:
        DB_CURSOR.execute("""SELECT day_of_departure, flight_fare_flight_1, flight_fare_flight_2, 
                          time_of_departure_flight_1, time_of_departure_flight_2 FROM Flights 
                          WHERE arrival_airport = ? GROUP BY day_of_departure""", (destination,))
        rows = DB_CURSOR.fetchall()
        print(rows)

        WEEKDAYS = {'po': 1, 'út': 2, 'st': 3, 'čt': 4, 'pá': 5, 'so': 6, 'ne': 7}
        rows.sort(key=lambda x: WEEKDAYS[x[0]])

        day_of_departure = []
        flight_fare_flight_1 = []
        flight_fare_flight_2 = []
        time_of_departure_flight_1 = []
        time_of_departure_flight_2 = []

        for row in rows:
            day_of_departure.append(row[0])
            flight_fare_flight_1.append(row[1])
            flight_fare_flight_2.append(row[2])
            time_of_departure_flight_1.append(row[3])
            time_of_departure_flight_2.append(row[4])

        line_chart = pygal.Line(title=f'Prices of flights PRG -> {destination} '
                                      f'by departure time as of 27th January 2019 (in CZK)',
                                print_values=False)
        line_chart.add('Day of departure', day_of_departure)
        line_chart.add('Flight fare of the first flight', flight_fare_flight_1)
        line_chart.add('Flight fare of the second flight', flight_fare_flight_2)
        line_chart.x_labels = time_of_departure_flight_1, time_of_departure_flight_2
        line_chart.render_to_file(f'line_chart_daily_price_PRG_{destination}_{TIMESTAMP}.svg')

# TODO: price change with departure date approaching
# TODO: length of overstay correlation with whole price
# TODO: price + length of stay + probability of being late - vyhodnostni index
# TODO: convenient hours of arrival - most frequent hours of arrival (+vyhodnostni index)
# TODO: seats for lower price correlations (true or not, what change will come afterwards)


def create_charts():
    day_of_purchase_chart()
    day_of_departure_chart()
    airlines_avg_price_chart()
    daily_price_chart()
    price_by_hours_chart()

