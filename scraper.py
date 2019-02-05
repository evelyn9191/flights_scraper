#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
import pandas as pd
import numpy as np


class FlightsSpider(CrawlSpider):
    """Create scraping spider."""
    name = 'flights_spider'
    custom_settings = {
        'DOWNLOAD_DELAY': 5,
    }

    def urls_to_scrape():
        """Make list with URLs to be scraped based on destinations and dates of flights."""
        start_urls = []

        target_destinations = [
            # PRG -> FAO
            '&srcTypedText=prg&srcFreeTypedText=&srcMC=&srcFreeAirport='
            '&dstAirport=Faro+%5BFAO%5D&dstTypedText=faro',
            # PRG -> KEF
            '&srcTypedText=prg&srcFreeTypedText=&srcMC=&srcFreeAirport='
            '&dstAirport=Reykjavik+%28Keflavik%29+%5BKEF%5D',
            # PRG -> TOS
            '&srcTypedText=prg&srcFreeTypedText=&srcMC=&srcFreeAirport='
            '&dstAirport=Tromso+%5BTOS%5D&dstTypedText=tromso',
            # PRG -> NCE
            '&srcTypedText=prg&srcFreeTypedText=&srcMC=&srcFreeAirport='
            '&dstAirport=Nice+%5BNCE%5D&dstTypedText=nice',
            # FAO -> PRG
            '&srcAirport=Faro+%5BFAO%5D&srcTypedText=fao'
            '&srcFreeTypedText=&srcMC=&srcFreeAirport='
            '&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg',
            # KEF -> PRG
            '&srcAirport=Reykjavik+%28Keflavik%29+%5BKEF%5D&srcTypedText=kef'
            '&srcFreeTypedText=&srcMC=&srcFreeAirport='
            '&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg',
            # TOS -> PRG
            '&srcAirport=Tromso+%5BTOS%5D&srcTypedText=tos'
            '&srcFreeTypedText=&srcMC=&srcFreeAirport='
            '&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg',
            # NCE -> PRG
            '&srcAirport=Nice+%5BNCE%5D&srcTypedText=nce'
            '&srcFreeTypedText=&srcMC=&srcFreeAirport='
            '&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg',
            # LIS -> PRG
            '&srcAirport=Lisabon+%5BLIS%5D&srcTypedText=lis'
            '&srcFreeTypedText=&srcMC=&srcFreeAirport='
            '&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg'
        ]

        tomorrow = datetime.now() + timedelta(days=1)
        timestamp = tomorrow.strftime("%#d.%#m.%Y")

        dates_range = [
            '&dstFreeAirport=&depdate=%s&arrdate=30.6.2019' % timestamp,
            '&dstFreeAirport=&depdate=1.7.2019&arrdate=30.11.2019'
        ]

        for destination in target_destinations:
            for date_range in dates_range:
                start_urls.append(
                    'http://www.azair.cz/azfin.php?tp=0&searchtype=flexi&srcAirport=Praha+%5BPRG%5D'
                    '&srcTypedText=prg&srcFreeTypedText=&srcMC=&srcFreeAirport='
                    + str(destination) +
                    '&dstFreeTypedText=&dstMC=&adults=1&children=0&infants=0'
                    '&minHourStay=0%3A45&maxHourStay=23%3A20'
                    '&minHourOutbound=0%3A00&maxHourOutbound=24%3A00'
                    '&minHourInbound=0%3A00&maxHourInbound=24%3A00'
                    + str(date_range) +
                    '&minDaysStay=3&maxDaysStay=9'
                    '&nextday=0&autoprice=true&currency=CZK'
                    '&wizzxclub=false&supervolotea=false&schengen=false&transfer=false'
                    '&samedep=true&samearr=false&dep0=true'
                    '&dep1=true&dep2=true&dep3=true&dep4=true&dep5=true&dep6=true'
                    '&arr0=true&arr1=true&arr2=true&arr3=true&arr4=true&arr5=true&arr6=true'
                    '&maxChng=1&isOneway=oneway&resultSubmit=Hledat#')
        return start_urls

    start_urls = urls_to_scrape()

    def parse(self, response):
        """Define items to look for in scraped website."""

        SET_SELECTOR = '.result '

        for flight_info_box in response.css(SET_SELECTOR):
            aer_code = '.code ::text'
            dept_date = '.date ::text'
            dept_time = '.from ::text'
            airlines = '.airline ::text'
            arr_time = '.to ::text'
            duration = '.durcha ::text'
            whole_price = '.subPrice ::text'
            price_for_sep_fl = '.legPrice ::text'
            seats_for_given_price = '.icoSeatWrapper ::text'

            yield {
                'date_of_departure': flight_info_box.css(dept_date).extract_first(),
                'departure_airport': flight_info_box.css(aer_code).extract_first(),
                'time_of_departure': flight_info_box.css(dept_time).extract_first(),
                'arrival_airport': flight_info_box.css(aer_code).extract()[1],
                'time_of_arrival': flight_info_box.css(arr_time).extract_first(),
                'flight_duration': flight_info_box.css(duration).extract_first(),
                'flight_fare': flight_info_box.css(whole_price).extract_first(),

                'departure_airport_flight_1': flight_info_box.css(aer_code).extract_first(),
                'time_of_departure_flight_1': flight_info_box.css(dept_time).extract_first(),
                'arrival_airport_flight_1': flight_info_box.css(aer_code).extract()[1],
                'time_of_arrival_flight_1': flight_info_box.css(arr_time).extract()[2],
                'airlines_flight_1': flight_info_box.css(airlines).extract_first(),
                'flight_fare_flight_1': flight_info_box.css(price_for_sep_fl).extract_first(),
                'seats_for_lower_price_flight_1': flight_info_box.css(
                    seats_for_given_price).extract_first(),

                'departure_airport_flight_2': flight_info_box.css(aer_code).extract()[4],
                'time_of_departure_flight_2': flight_info_box.css(dept_time)[5].extract(),
                'arrival_airport_flight_2': flight_info_box.css(aer_code).extract()[1],
                'time_of_arrival_flight_2': flight_info_box.css(arr_time).extract_first(),
                'airlines_flight_2': flight_info_box.css(airlines).extract()[1],
                'flight_fare_flight_2': flight_info_box.css(price_for_sep_fl).extract()[1],
                'seats_for_lower_price_flight_2': flight_info_box.css(
                    seats_for_given_price).extract()[1]
            }


def run_spider():
    """Run FlightsSpider and give output in .csv format."""
    timestamp = datetime.now().strftime("%d.%m.%Y")
    csv_output_file = f'flights_{timestamp}.csv'
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'csv',
        'FEED_URI': csv_output_file
    })
    process.crawl(FlightsSpider)
    process.start()

    return csv_output_file


def edit_data(path_to_data):
    """Format data as needed and return .csv file.

    :param path_to_data: Path to the exported file with data on flights.
    :return output_file: Path to the exported file with correct formatting.
    """
    df = pd.read_csv(path_to_data, error_bad_lines=False)

    # Add index column name
    df.index.name = 'uid'

    # Split columns with incorrect formatting
    df['date_of_download'] = datetime.now().strftime("%d.%m.%Y")
    df['day_of_download'] = datetime.now().strftime("%A")

    dept = df['date_of_departure'].str.split("\s", n=1, expand=True)
    df['date_of_departure'] = dept[1]
    df['day_of_departure'] = dept[0]

    # Convert Czech words to English
    weekdays = {'po': 'Monday', 'út': 'Tuesday', 'st': 'Wednesday',
                'čt': 'Thursday', 'pá': 'Friday', 'so': 'Saturday', 'ne': 'Sunday'}
    df['day_of_departure'].apply(lambda x: x.replace(x, weekdays[x]))
    # TODO: shortened from: (check if working)
    #  weekday_name = df['day_of_departure'].apply(lambda x: x.replace(x, weekdays[x]))
    #  df['day_of_departure'] = weekday_name

    # Split columns with incorrect formatting
    arrival_columns = ['time_of_arrival', 'time_of_arrival_flight_1',
                       'time_of_arrival_flight_2']
    for arrival_column in arrival_columns:
        arrival = df[arrival_column].str.split('\s', n=1, expand=True)
        df[arrival_column] = arrival[0]

    duration = df['flight_duration'].str.split('\s', n=1, expand=True)
    df['flight_duration'] = duration[0]

    fare_columns = ['flight_fare', 'flight_fare_flight_1', 'flight_fare_flight_2']
    for fare_column in fare_columns:
        fare = df[fare_column].str.split('\s', n=1, expand=True)
        df[fare_column] = fare[0]

    # Replace unneeded whitespace
    seats_for_lower_price_columns = ['seats_for_lower_price_flight_1',
                                     'seats_for_lower_price_flight_2']
    for seats_column in seats_for_lower_price_columns:
        seat = df[seats_column].str.replace('       ', '')
        df[seats_column] = seat

    # Use only airport code to define airport
    kef_airport_columns_fix = ['arrival_airport', 'arrival_airport_flight_1',
                               'arrival_airport_flight_2', 'departure_airport_flight_2']
    for column_name in kef_airport_columns_fix:
        airport_code = df[column_name].str[-3:]
        df[column_name] = airport_code

    # Split columns with incorrect formatting
    clean_departure_time = df['time_of_departure_flight_2'].str.split('\s', n=2, expand=True)
    df['time_of_departure_flight_2'] = clean_departure_time[1]

    # If both columns contain 'KEF', change arrival airport to PRG and airport name
    # where flights are changed to 'unknown'
    df['arrival_airport_flight_1'] = np.where((df['departure_airport'] == 'KEF')
                                              & (df['arrival_airport'] == 'KEF'),
                                              '', df['arrival_airport_flight_1'])

    df['departure_airport_flight_2'] = np.where((df['departure_airport'] == 'KEF')
                                                & (df['arrival_airport'] == 'KEF'),
                                                '', df['departure_airport_flight_2'])

    df['arrival_airport'] = np.where((df['departure_airport'] == 'KEF')
                                     & (df['arrival_airport'] == 'KEF'),
                                     'PRG', df['arrival_airport'])

    # Rewrite rows containing 'Reykjavik' word with estimated time of arrival
    # for the first flights to Reykjavik, based on set estimated duration of
    # 1 hour and 10 minutes.
    formatted_arrival_time = df.loc[:, 'time_of_departure_flight_1'].apply(
        lambda x: datetime.strptime(x, '%H:%M'))  # TODO: ValueError: time data 'time_of_departure_flight_1' does not match format '%H:%M' - obsahuje uknown. Smazano
    estimated_arrival_time = formatted_arrival_time + timedelta(hours=1, minutes=10)
    wrong_data = df.loc[:, 'time_of_arrival_flight_1'].apply(lambda x: 'Reykjavik' in x)
    df['time_of_arrival_flight_1'] = np.where(
        wrong_data,
        estimated_arrival_time.apply(lambda x: datetime.strftime(x, '%H:%M')),
        df['time_of_arrival_flight_1']
    )

    # Adjust formatting
    df['airlines_flight_2'] = np.where(df['airlines_flight_2'] == 'Transavia France',
                                     'Transavia', df['airlines_flight_2'])
    df['time_of_departure'].apply(lambda x: datetime.strptime(x, '%H:%M'))    # TODO: ValueError: time data 'time_of_departure' does not match format '%H:%M'  - obsahuje uknown. Smazano

    # Delete rows that contain header except for the main header
    df = df[~df['departure_airport'].str.contains("departure_airport")]

    # Remove unneeded columns for flights without change (case of Czech Airlines flights)
    for value in df['flight_fare']:
        if value in df['flight_fare_flight_1']:
            df['departure_airport_flight_2':].remove()

    # Save edited file
    df.to_csv(path_to_data, sep='|', encoding='utf-8', index=True)

    return path_to_data
