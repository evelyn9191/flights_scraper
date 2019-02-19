#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import pygal

import pandas as pd

from database import DB_CURSOR, DB_CONNECTION

TIMESTAMP = datetime.now().strftime('%#d-%#m-%#Y')
SAVING_DIR = datetime.now().strftime('%B_%Y')
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
        f'exported_charts/{SAVING_DIR}/day_of_purchase_{TIMESTAMP}.svg')

    best_day = sorted(rows, key=lambda x: (x[0] + x[1]))

    print(f'The best days to buy tickets are:\n'
          f'1. {best_day[0][2]}\n'
          f'2. {best_day[1][2]}\n'
          f'3. {best_day[2][2]}\n'
          f'4. {best_day[3][2]}\n'
          f'5. {best_day[4][2]}\n'
          f'6. {best_day[5][2]}\n'
          f'7. {best_day[6][2]}\n'
          )

    return day_of_purchase_final_chart


def day_of_departure_chart():
    """Chart about average prices of flight tickets based on departure weekday."""
    DB_CURSOR.execute('SELECT ROUND(avg(flight_fare_flight_1), 2), '
                      'ROUND(avg(flight_fare_flight_2), 2), day_of_departure '
                      'FROM Flights GROUP BY day_of_departure')

    rows = DB_CURSOR.fetchall()

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
        f'exported_charts/{SAVING_DIR}/day_of_departure_line_{TIMESTAMP}.svg')

    for index, value in enumerate(flight_fare_flight_1):
        percentage_difference = round((100 * flight_fare_flight_2[index]) / value - 100, 1)
        print(f'Percentage change for {day_of_departure[index]}: {percentage_difference}%')

    best_day = sorted(rows, key=lambda x: (x[0] + x[1]))

    print(f'The best days for flight departure are:\n'
          f'1. {best_day[0][2]}\n'
          f'2. {best_day[1][2]}\n'
          f'3. {best_day[2][2]}\n'
          f'4. {best_day[3][2]}\n'
          f'5. {best_day[4][2]}\n'
          f'6. {best_day[5][2]}\n'
          f'7. {best_day[6][2]}\n'
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
                          width=1500,
                          print_values=True, print_values_position='top')
    bar_chart.add('First flight average price', final_flight_fare_flight_1)
    bar_chart.add('Second flight average price', final_flight_fare_flight_2)
    bar_chart.x_labels = final_airlines
    airlines_avg_price_final_chart = bar_chart.render_to_file(
        f'exported_charts/{SAVING_DIR}/airlines_avg_price_{TIMESTAMP}.svg')

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
                              width=1500, print_values=False, show_x_labels=False)
        bar_chart.add('Flight fare', flight_fare)
        bar_chart.x_labels = date_of_departure
        bar_chart.render_to_file(f'exported_charts/{SAVING_DIR}/'
                                 f'daily_price_PRG_{destination}_{TIMESTAMP}.svg')

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
                              width=1500, print_values=False, show_x_labels=False)
        bar_chart.add('Flight fare', flight_fare)
        bar_chart.x_labels = date_of_departure
        bar_chart.render_to_file(f'exported_charts/{SAVING_DIR}/'
                                 f'daily_price_{destination}_PRG_{TIMESTAMP}.svg')


def price_change_chart(dates_to_compare_prices):
    """Chart about price changes caused by approaching departure date."""
    arrival_destinations = ['FAO', 'KEF', 'NCE', 'TOS']
    departure_destinations = ['LIS', 'FAO', 'KEF', 'NCE', 'TOS']

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
            line_chart.add(f'Flight fares by {relevant_dates[position]}', all_flight_fares[position])
            line_chart.x_labels = all_departure_times[position]
        try:
            line_chart.y_labels = all_flight_fares[0]
            line_chart.render_to_file(f'exported_charts/{SAVING_DIR}/'
                                      f'price_by_departure_time_PRG_{destination}_{TIMESTAMP}.svg')
        except IndexError:
            print(f'Chart about price changes caused by approaching departure date for flight '
                  f'PRG -> {destination} wasn\'t exported.')

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
            line_chart.add(f'Flight fares by {relevant_dates[position]}', all_flight_fares[position])
            line_chart.x_labels = all_departure_times[position]
        try:
            line_chart.y_labels = all_flight_fares[0]
            line_chart.render_to_file(f'exported_charts/{SAVING_DIR}/'
                                      f'price_by_departure_time_{destination}_PRG_{TIMESTAMP}.svg')
        except IndexError:
            print(f'Chart about price changes caused by approaching departure date for flight ' 
                  f'{destination}-> PRG wasn\'t exported.')


def prices_by_departure_time_chart():
    """Chart about average prices of flight tickets based on time of departure."""
    arrival_destinations = ['FAO', 'KEF', 'NCE', 'TOS']
    departure_destinations = ['LIS', 'FAO', 'KEF', 'NCE', 'TOS']
    arrival_monitored_dates = {'FAO': '20.5.2019', 'KEF': '21.09.2019',
                               'NCE': '25.05.2019', 'TOS': '25.08.2019'}
    departure_monitored_dates = {'LIS': '24.07.2019', 'FAO': '30.09.2019', 'KEF': '30.09.2019',
                                 'NCE': '22.07.2019', 'TOS': '18.09.2019'}

    for destination in arrival_destinations:
        DB_CURSOR.execute("""SELECT flight_fare, time_of_departure 
                          FROM Flights WHERE arrival_airport = ? AND date_of_departure = ?
                          GROUP BY time_of_departure""", (destination, arrival_monitored_dates[destination]))
        rows = DB_CURSOR.fetchall()

        rows.sort(key=lambda x: x[1])

        flight_fare = []
        time_of_departure = []

        for row in rows:
            flight_fare.append(row[0])
            time_of_departure.append(row[1])

        if len(time_of_departure) > 1:
            bar_chart = pygal.Bar(title=f'Prices of flights PRG -> {destination} '
            f'by departure time (in CZK)',
                                    print_values=False, x_title='Time of departure')
            bar_chart.add('Flight fare', flight_fare)
            bar_chart.x_labels = time_of_departure
            bar_chart.render_to_file(f'exported_charts/{SAVING_DIR}/'
                                     f'daily_price_PRG_{destination}_{TIMESTAMP}.svg')

    for destination in departure_destinations:
        DB_CURSOR.execute("""SELECT flight_fare, time_of_departure 
                          FROM Flights WHERE departure_airport = ? AND date_of_departure = ?
                          GROUP BY time_of_departure""", (destination, departure_monitored_dates[destination]))
        rows = DB_CURSOR.fetchall()

        rows.sort(key=lambda x: x[1])

        flight_fare = []
        time_of_departure = []

        for row in rows:
            flight_fare.append(row[0])
            time_of_departure.append(row[1])

        if len(time_of_departure) > 1:
            bar_chart = pygal.Bar(title=f'Prices of flights {destination} -> PRG '
                                        f'by departure time (in CZK)',
                                  print_values=False, x_title='Time of departure')
            bar_chart.add('Flight fare', flight_fare)
            bar_chart.x_labels = time_of_departure
            bar_chart.render_to_file(f'exported_charts/{SAVING_DIR}/'
                                     f'daily_price_{destination}_PRG_{TIMESTAMP}.svg')


def cheap_seats_chart():
    """Chart about change of price based on cheap seats tickets purchase."""
    arrival_destinations = ['FAO', 'KEF', 'NCE']
    departure_destinations = ['LIS', 'FAO', 'KEF', 'NCE']
    arrival_monitored_dates = {'FAO': '02.04.2019', 'KEF': '02.04.2019',
                               'NCE': '15.03.2019'}
    departure_monitored_dates = {'LIS': '02.04.2019', 'FAO': '01.04.2019',
                                 'KEF': '02.05.2019', 'NCE': '01.04.2019'}

    for destination in arrival_destinations:
        select_query = f"""SELECT date_of_download, date_of_departure, time_of_departure, 
                        flight_fare_flight_2, seats_for_lower_price_flight_2 
                        FROM Flights WHERE date_of_departure='{arrival_monitored_dates[destination]}'
                        AND arrival_airport='{destination}' 
                        ORDER BY time_of_departure ASC"""
        df = pd.read_sql_query(select_query, DB_CONNECTION)

        df['date_of_download'].apply(lambda x: datetime.strptime(x, '%d.%m.%Y'))
        df['date_of_departure'].apply(lambda x: datetime.strptime(x, '%d.%m.%Y'))

        # Slight workaround - it wasn't working when formatted using regular ways
        df['seats_for_lower_price_flight_2'].fillna(0, inplace=True)
        no_nan_df = df[~df['seats_for_lower_price_flight_2'].isnull()]
        df['seats_for_lower_price_flight_2'] = no_nan_df['seats_for_lower_price_flight_2'].astype(int)
        df['seats_for_lower_price_flight_2'].mask(df['seats_for_lower_price_flight_2'] == 0, '', inplace=True)

        # TODO: fix working of this part
        df.groupby('time_of_departure')
        #print(df.head(10))
        df['group_number'] = df.groupby('time_of_departure').ngroup()
        df['group_number'] = df['group_number'].apply(lambda x: x % 2)

        def highlight_values():
            if df.loc['group_number'] == 0:
                print('yes')
                colour = 'green'
            else:
                print('no')
                colour = 'red'
            return 'background-color: %s' % colour

        df.style.applymap(highlight_values)
        #print(df.head(8))

        df.to_html(f'exported_charts/{SAVING_DIR}/cheaper_seats_PRG_{destination}_table.html')

    for destination in departure_destinations:
        select_query = f"""SELECT date_of_download, date_of_departure, time_of_departure, 
                        flight_fare_flight_2, seats_for_lower_price_flight_2 
                        FROM Flights WHERE date_of_departure='{departure_monitored_dates[destination]}'
                        AND departure_airport='{destination}' 
                        ORDER BY time_of_departure ASC"""
        df = pd.read_sql_query(select_query, DB_CONNECTION, coerce_float=False,
                               parse_dates={'date_of_download': '%d.%m.%Y'})
        df.to_html(f'exported_charts/{SAVING_DIR}/cheaper_seats_{destination}_PRG_table.html')


def create_charts():
    day_of_purchase_chart()
    day_of_departure_chart()
    airlines_avg_price_chart()
    daily_price_chart()

    dates_to_compare_prices = ['10.02.2019', '01.03.2019', '01.04.2019', '01.05.2019',
                               '01.06.2019', '01.07.2019', '20.07.2019']
    for date in dates_to_compare_prices:
        date = datetime.strptime(date, '%d.%m.%Y').strftime('%d-%m-%Y')
        if date == TIMESTAMP:
            price_change_chart(dates_to_compare_prices)

    prices_by_departure_time_chart()
    cheap_seats_chart()


if __name__ == "__main___":
    create_charts()
    print('Charts successfully created.')
