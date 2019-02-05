#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import pygal

from database import DB_CURSOR

# Set time period that will be analyzed
ANALYZED_PERIOD_START = '15.03.2019'
ANALYZED_PERIOD_FINISH = '30.11.2019'

# Define other variables
TIMESTAMP = datetime.now().strftime('%#d-%#m-%#Y')
WEEKDAYS = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3,
            'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}


def day_of_purchase_chart():
    """Chart about average prices of flight tickets based on weekday when they are bought."""
    DB_CURSOR.execute('SELECT ROUND(avg(flight_fare_flight_1), 2), '
                      'ROUND(avg(flight_fare_flight_2), 2), day_of_download '
                      'FROM Flights GROUP BY day_of_download')

    rows = DB_CURSOR.fetchall()

    rows.sort(key=lambda x: WEEKDAYS[x[2]])

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
        f'day_of_purchase_{TIMESTAMP}.svg')

    return day_of_purchase_final_chart


def day_of_departure_chart():
    """Chart about average prices of flight tickets based on departure weekday."""
    DB_CURSOR.execute('SELECT ROUND(avg(flight_fare_flight_1), 2), '
                      'ROUND(avg(flight_fare_flight_2), 2), day_of_departure '
                      'FROM Flights GROUP BY day_of_departure')

    rows = DB_CURSOR.fetchall()

    rows.sort(key=lambda x: WEEKDAYS[x[2]])
    print(rows)

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
        f'day_of_departure_line_{TIMESTAMP}.svg')

    for index, value in enumerate(flight_fare_flight_1):
        percentage_difference = round((100 * flight_fare_flight_2[index]) / value - 100, 1)
        print(f'Percentage change for {day_of_departure[index]}: {percentage_difference}%')

    flight_1_asc = sorted(rows, key=lambda x: x[0])
    flight_2_asc = sorted(rows, key=lambda x: x[1])

    print(f'The best days to buy tickets for the first flight are:\n'
          f'1. {flight_1_asc[0][2]}\n'
          f'2. {flight_1_asc[1][2]}\n'
          f'3. {flight_1_asc[2][2]}\n'
          f'4. {flight_1_asc[3][2]}\n'
          f'5. {flight_1_asc[4][2]}\n'
          f'6. {flight_1_asc[5][2]}\n'
          f'7. {flight_1_asc[6][2]}\n'
          )
    print('The best days to buy tickets for the second flight are:\n'
          f'1. {flight_2_asc[0][2]}\n'
          f'2. {flight_2_asc[1][2]}\n'
          f'3. {flight_2_asc[2][2]}\n'
          f'4. {flight_2_asc[3][2]}\n'
          f'5. {flight_2_asc[4][2]}\n'
          f'6. {flight_2_asc[5][2]}\n'
          f'7. {flight_2_asc[6][2]}\n'
          )

    return day_of_departure_final_chart


def airlines_avg_price_chart():
    """Chart about average prices of flight tickets based on airlines."""
    DB_CURSOR.execute('SELECT ROUND(avg(flight_fare_flight_1), 2), airlines_flight_1 '
                      'FROM Flights GROUP BY airlines_flight_1')
    flights_1_data = DB_CURSOR.fetchall()

    DB_CURSOR.execute('SELECT ROUND(avg(flight_fare_flight_2), 2), airlines_flight_2 '
                      'FROM Flights GROUP BY airlines_flight_2')
    flights_2_data = DB_CURSOR.fetchall()

    flight_fare_flight_1 = []
    flight_fare_flight_2 = []
    airlines_flight_1 = []
    airlines_flight_2 = []

    for row in flights_1_data:
        flight_fare_flight_1.append(row[0])
        airlines_flight_1.append(row[1])

    for row in flights_2_data:
        flight_fare_flight_2.append(row[0])
        airlines_flight_2.append(row[1])

    # Adjust lists to contain all the airlines and add value 0 for each of the missing ones
    for airline in airlines_flight_1:
        if airline not in airlines_flight_2:
            airlines_flight_2.append(airline)
            flight_fare_flight_2.append(0)

    for airline in airlines_flight_2:
        if airline not in airlines_flight_1:
            airlines_flight_1.append(airline)
            flight_fare_flight_1.append(0)

    # Make list of tuples with correct values for respective airlines
    matched_data = []
    for i, airline in enumerate(airlines_flight_1):
        index_airline_flight_2 = airlines_flight_2.index(airline)
        matched_data.append((airline, flight_fare_flight_1[i], flight_fare_flight_2[index_airline_flight_2]))
    matched_data.sort(key=lambda x: x[0].upper())

    # Split tuples to lists to provide data for Pygal
    final_flight_fare_flight_1 = []
    final_flight_fare_flight_2 = []
    final_airlines = []

    for row in matched_data:
        final_airlines.append(row[0])
        final_flight_fare_flight_1.append(row[1])
        final_flight_fare_flight_2.append(row[2])

    # Render chart
    bar_chart = pygal.Bar(title='Average price of flight ticket '
                                'based on airlines (in CZK)',
                          print_values=True, print_values_position='top')
    bar_chart.add('First flight average price', final_flight_fare_flight_1)
    bar_chart.add('Second flight average price', final_flight_fare_flight_2)
    bar_chart.x_labels = final_airlines
    airlines_avg_price_final_chart = bar_chart.render_to_file(
        f'airlines_avg_price_{TIMESTAMP}.svg')

    return airlines_avg_price_final_chart


def daily_price_chart():
    """Chart about average prices of flight tickets by date of departure."""
    arrival_destinations = ['FAO', 'KEF', 'NCE', 'TOS']
    departure_destinations = ['LIS', 'FAO', 'KEF', 'NCE', 'TOS']

    for destination in arrival_destinations:
        DB_CURSOR.execute("""SELECT ROUND(flight_fare, 2), date_of_departure '
                          'FROM Flights WHERE arrival_airport = ? AND date_of_departure 
                          BETWEEN '15.03.2019' AND '31.11.2019'""", (destination,))

        rows = DB_CURSOR.fetchall()

        rows.sort(key=lambda x: datetime.strptime(x[1], '%d.%m.%Y'))

        flight_fare = []
        date_of_departure = []

        for row in rows:
            flight_fare.append(row[0])
            date_of_departure.append(row[1])

        bar_chart = pygal.Bar(title=f'Prices of flights PRG -> {destination} '
                                    f'by date of departure (in CZK)',
                              print_values=False)
        bar_chart.add('Flight fare', flight_fare)
        bar_chart.x_labels = date_of_departure
        bar_chart.render_to_file(f'daily_price_PRG_{destination}_{TIMESTAMP}.svg')

    for destination in departure_destinations:
        DB_CURSOR.execute("""SELECT ROUND(flight_fare, 2), date_of_departure '
                          'FROM Flights WHERE departure_airport = ? AND date_of_departure 
                          BETWEEN '15.03.2019' AND '31.11.2019'""", (destination,))

        rows = DB_CURSOR.fetchall()

        rows.sort(key=lambda x: datetime.strptime(x[1], '%d.%m.%Y'))

        flight_fare = []
        date_of_departure = []

        for row in rows:
            flight_fare.append(row[0])
            date_of_departure.append(row[1])

        bar_chart = pygal.Bar(title=f'Prices of flights {destination} -> PRG '
                                    f'by date of departure (in CZK)',
                              print_values=False)
        bar_chart.add('Flight fare', flight_fare)
        bar_chart.x_labels = date_of_departure
        bar_chart.render_to_file(f'daily_price_{destination}_PRG_{TIMESTAMP}.svg')


def price_by_hours_chart():
    """Chart about average prices of flight tickets based on daily time of departure."""
    arrival_destinations = ['FAO', 'KEF', 'NCE', 'TOS']
    departure_destinations = ['LIS', 'FAO', 'KEF', 'NCE', 'TOS']
    dates_to_compare_prices = ['1.2.2019', '05.02.2019', '01.03.2019', '01.04.2019', '01.05.2019',
                               '01.06.2019', '01.07.2019', '20.07.2019']

    relevant_dates = []
    for date_to_compare in dates_to_compare_prices:
        if datetime.strptime(date_to_compare, '%d.%m.%Y').date() <= datetime.now().date():
            relevant_dates.append(date_to_compare)

    for destination in arrival_destinations:
        all_flight_fares = []
        all_departure_times = []
        for relevant_date in relevant_dates:
            DB_CURSOR.execute("""SELECT flight_fare, time_of_departure_flight_1
                              FROM Flights WHERE date_of_download = ? AND
                              arrival_airport = ? AND
                              date_of_departure BETWEEN '22.07.2019' AND '28.7.2019'
                              """, (relevant_date, destination))
            rows = DB_CURSOR.fetchall()

            # Sort by time of departure
            rows.sort(key=lambda x: datetime.strptime(x[1], '%H:%M'))

            flight_fare = []
            time_of_departure = []

            for row in rows:
                flight_fare.append(row[0])
                time_of_departure.append(datetime.strptime(row[1], '%H:%M').strftime('%H:%M'))

            all_flight_fares.append(flight_fare)
            all_departure_times.append(time_of_departure)

        line_chart = pygal.Line(title=f'Prices of flights PRG -> {destination} by '
                                      f'time of departure between 22/07/2019 and 28/07/2019(in CZK)',
                                width=1500, x_title='Daytime of departure', y_title='Prices',
                                stroke=False, x_label_rotation=20,
                                y_labels_major_every=25, show_minor_y_labels=False,
                                show_x_labels=False)

        for position in range(0, len(all_flight_fares)):
            line_chart.add(f'Flight fares by {relevant_dates[position]}', all_flight_fares[position]) #[{'value': all_flight_fares[position]}])
            # line_chart.add(f'Flight fares by {relevant_dates[position]}', all_flight_fares[position])
            line_chart.x_labels = all_departure_times[position]    # Departure times are always the same
        line_chart.y_labels = all_flight_fares[0]    # Pick one list for y labels is enough
        line_chart.render_to_file(f'price_by_departure_time_PRG_{destination}_{TIMESTAMP}.svg')

    for destination in departure_destinations:
        all_flight_fares = []
        all_departure_times = []
        for relevant_date in relevant_dates:
            DB_CURSOR.execute("""SELECT flight_fare, time_of_departure_flight_1
                              FROM Flights WHERE date_of_download = ? AND
                              departure_airport = ? AND
                              date_of_departure BETWEEN '22.07.2019' AND '28.7.2019'
                              """, (relevant_date, destination))
            rows = DB_CURSOR.fetchall()

            # Sort by time of departure
            rows.sort(key=lambda x: datetime.strptime(x[1], '%H:%M'))

            flight_fare = []
            time_of_departure = []

            for row in rows:
                flight_fare.append(row[0])
                time_of_departure.append(datetime.strptime(row[1], '%H:%M').strftime('%H:%M'))

            all_flight_fares.append(flight_fare)
            all_departure_times.append(time_of_departure)

        line_chart = pygal.Line(title=f'Prices of flights {destination} -> PRG by '
                                      f'time of departure between 22/07/2019 and 28/07/2019(in CZK)',
                                width=1500, x_title='Daytime of departure', y_title='Prices',
                                stroke=False, x_label_rotation=20,
                                y_labels_major_every=25, show_minor_y_labels=False,
                                show_x_labels=False)

        for position in range(0, len(all_flight_fares)):
            line_chart.add(f'Flight fares by {relevant_dates[position]}', all_flight_fares[position]) #[{'value': all_flight_fares[position]}])
            # line_chart.add(f'Flight fares by {relevant_dates[position]}', all_flight_fares[position])
            line_chart.x_labels = all_departure_times[position]    # Departure times are always the same
        line_chart.y_labels = all_flight_fares[0]    # Pick one list for y labels is enough
        line_chart.render_to_file(f'price_by_departure_time_{destination}_PRG_{TIMESTAMP}.svg')


def price_change_chart():
    """Chart about price change based on approaching date of departure."""
    # TODO: did not start working on this one yet
    arrival_destinations = ['FAO', 'KEF', 'NCE', 'TOS']
    # PRG -> FAO 20.5.
    # PRG -> KEF 21.9.
    # PRG -> NCE 25.5.
    # PRG -> TOS 25.8.
    # departure_destinations = ['LIS']

    for destination in arrival_destinations:
        DB_CURSOR.execute("""SELECT day_of_departure, flight_fare_flight_1, flight_fare_flight_2, 
                              time_of_departure_flight_1, time_of_departure_flight_2 FROM Flights 
                              WHERE arrival_airport = ? GROUP BY day_of_departure""", (destination,))
        rows = DB_CURSOR.fetchall()
        print(rows)

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
        line_chart.render_to_file(f'daily_price_PRG_{destination}_{TIMESTAMP}.svg')


# TODO: seats for lower price correlations (true or not, what change will come afterwards)


def create_charts():
    day_of_purchase_chart()
    day_of_departure_chart()
    airlines_avg_price_chart()
    daily_price_chart()
    price_by_hours_chart()    # TODO: run on certain dates only
