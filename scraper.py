#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
import pandas as pd

from database import DB_CURSOR, import_to_database, create_database


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
            '&srcTypedText=prg&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Faro+%5BFAO%5D&dstTypedText=faro',
            # PRG -> KEF
            '&srcTypedText=prg&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Reykjavik+%28Keflavik%29+%5BKEF%5D',
            # PRG -> TOS
            '&srcTypedText=prg&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Tromso+%5BTOS%5D&dstTypedText=tromso',
            # PRG -> NCE
            '&srcTypedText=prg&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Nice+%5BNCE%5D&dstTypedText=nice',
            # FAO -> PRG
            '&srcAirport=Faro+%5BFAO%5D&srcTypedText=fao&srcFreeTypedText=&srcMC=&srcFreeAirport='
            '&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg'
            # KEF -> PRG
            '&srcAirport=Reykjavik+%28Keflavik%29+%5BKEF%5D&srcTypedText=kef&srcFreeTypedText=&srcMC=&srcFreeAirport='
            '&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg'
            # TOS -> PRG
            '&srcAirport=Tromso+%5BTOS%5D&srcTypedText=tos&srcFreeTypedText=&srcMC=&srcFreeAirport='
            '&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg'
            # NCE -> PRG
            '&srcAirport=Nice+%5BNCE%5D&srcTypedText=nce&srcFreeTypedText=&srcMC=&srcFreeAirport='
            '&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg'
            # LIS -> PRG
            '&srcAirport=Lisabon+%5BLIS%5D&srcTypedText=lis&srcFreeTypedText=&srcMC=&srcFreeAirport='
            '&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg'
        ]

        tomorrow = datetime.now() + timedelta(days=1)
        timestamp = tomorrow.strftime("%-d.%-m.%Y")

        dates_range = [
            '&dstFreeAirport=&depdate=%s&arrdate=30.6.2019' % timestamp,
            '&dstFreeAirport=&depdate=1.7.2019&arrdate=31.10.2019'
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
            DEPT_AER_CODE = '.code ::text'
            ARR_AER_CODE = '/html[1]/body[1]/div[5]/div[1]/div[1]/p[1]/span[4]/span[1]/text()'
            DEPT_DATE = '.date ::text'
            DEPT_TIME = '.from ::text'
            AIRLINES = '.airline ::text'
            ARR_TIME = '.to ::text'
            DURATION = '.durcha ::text'
            WHOLE_PRICE = '.subPrice ::text'
            PRICE_FOR_SEPARATE_FLIGHT = '.legPrice ::text'
            SEATS_FOR_GIVEN_PRICE = '.icoSeatWrapper ::text'

            yield {
                'date_of_departure': flight_info_box.css(DEPT_DATE).extract_first(),
                'departure_airport': flight_info_box.css(DEPT_AER_CODE).extract_first(),
                'time_of_departure': flight_info_box.css(DEPT_TIME).extract_first(),
                'arrival_airport': flight_info_box.xpath(ARR_AER_CODE).extract_first(),
                'time_of_arrival': flight_info_box.css(ARR_TIME).extract_first(),
                'flight_duration': flight_info_box.css(DURATION).extract_first(),
                'flight_fare': flight_info_box.css(WHOLE_PRICE).extract_first(),

                'departure_airport_flight_1': flight_info_box.css(DEPT_AER_CODE).extract()[2],
                'time_of_departure_flight_1': flight_info_box.css(DEPT_TIME).extract()[0],
                'arrival_airport_flight_1': flight_info_box.css(DEPT_AER_CODE).extract()[3],
                'time_of_arrival_flight_1': flight_info_box.css(ARR_TIME).extract()[2],
                'airlines_flight_1': flight_info_box.css(AIRLINES).extract_first(),
                'flight_fare_flight_1': flight_info_box.css(PRICE_FOR_SEPARATE_FLIGHT).extract()[0],
                'seats_for_lower_price_flight_1': flight_info_box.css(SEATS_FOR_GIVEN_PRICE).extract_first(),

                'departure_airport_flight_2': flight_info_box.css(DEPT_AER_CODE).extract()[3],
                'time_of_departure_flight_2': flight_info_box.css(DEPT_TIME).extract()[3],
                'arrival_airport_flight_2': flight_info_box.xpath(ARR_AER_CODE).extract_first(),
                'time_of_arrival_flight_2': flight_info_box.css(ARR_TIME).extract_first(),
                'airlines_flight_2': flight_info_box.css(AIRLINES).extract()[1],
                'flight_fare_flight_2': flight_info_box.css(PRICE_FOR_SEPARATE_FLIGHT).extract()[1],
                'seats_for_lower_price_flight_2': flight_info_box.css(SEATS_FOR_GIVEN_PRICE).extract()[1],
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
    """Format data as needed and return .csv file."""
    df = pd.read_csv(path_to_data, error_bad_lines=False)

    df.index.name = 'uid'
    df['date_of_download'] = datetime.now().strftime("%d.%m.%Y")
    df['day_of_download'] = datetime.now().strftime("%A")

    dept = df['date_of_departure'].str.split("\s", n=1, expand=True)
    df['day_of_departure'] = dept[0]
    df['date_of_departure'] = dept[1]

    arrival_columns = ['time_of_arrival', 'time_of_arrival_flight_1', 'time_of_arrival_flight_2']
    for arrival_column in arrival_columns:
        arrival = df[arrival_column].str.split('\s', n=1, expand=True)
        df[arrival_column] = arrival[0]

    duration = df['flight_duration'].str.split('\s', n=1, expand=True)
    df['flight_duration'] = duration[0]

    fare_columns = ['flight_fare', 'flight_fare_flight_1', 'flight_fare_flight_2']
    for fare_column in fare_columns:
        fare = df[fare_column].str.split('\s', n=1, expand=True)
        df[fare_column] = fare[0]

    seats_for_lower_price_columns = ['seats_for_lower_price_flight_1', 'seats_for_lower_price_flight_2']
    for seats_column in seats_for_lower_price_columns:
        seat = df[seats_column].str.replace('       ', '')
        df[seats_column] = seat

    clean_departure_time = df['time_of_departure_flight_2'].str.split('\s', n=2, expand=True)
    df['time_of_departure_flight_2'] = clean_departure_time[1]

    output_file = df.to_csv(path_to_data, sep='|', encoding='utf-8', index=True)

    return output_file


if __name__ == '__main__':
    path_to_csv = run_spider()
    edit_data(path_to_data=path_to_csv)
    create_database()
    import_to_database(path_to_data=path_to_csv)
    day_of_purchase_chart()
