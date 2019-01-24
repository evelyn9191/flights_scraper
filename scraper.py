#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import sqlite3
import logging
from datetime import datetime, timedelta

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class FlightsSpider(CrawlSpider):
    name = 'flights_spider'
    AUTOTHROTTLE_START_DELAY = 3
    AUTOTHROTTLE_MAX_DELAY = 7

    def urls_to_scrape(self):
        start_urls = []

        target_destinations = [
            # PRG -> FAO
            '&srcTypedText=prg&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Faro+%5BFAO%5D&dstTypedText=faro',
            # PRG -> KEF
            '&srcTypedText=prg&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Reykjavik+%28Keflavik%29+%5BKEF%5D',
            # PRG -> TOS
            '&srcTypedText=prg&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Tromso+%5BTOS%5D&dstTypedText=tromso',
            # PRG -> DUB
            '&srcTypedText=prg&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Dublin+%5BDUB%5D&dstTypedText=dublin',
            # PRG -> NCE
            '&srcTypedText=prg&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Nice+%5BNCE%5D&dstTypedText=nice',
            # FAO -> PRG
            '&srcAirport=Faro+%5BFAO%5D&srcTypedText=fao&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg'
            # KEF -> PRG
            '&srcAirport=Reykjavik+%28Keflavik%29+%5BKEF%5D&srcTypedText=kef&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg'
            # TOS -> PRG
            '&srcAirport=Tromso+%5BTOS%5D&srcTypedText=tos&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg'
            # DUB -> PRG
            '&srcAirport=Dublin+%5BDUB%5D&srcTypedText=dub&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg'
            # NCE -> PRG
            '&srcAirport=Nice+%5BNCE%5D&srcTypedText=nce&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg'
            # OPO -> PRG
            '&srcAirport=Porto+%5BOPO%5D&srcTypedText=porto&srcFreeTypedText=&srcMC=&srcap3=LIS&srcFreeAirport=&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg'
            # LIS -> PRG
            '&srcAirport=Lisabon+%5BLIS%5D&srcTypedText=lis&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Praha+%5BPRG%5D&dstTypedText=prg'
            # PRG -> JAP not on Azair
        ]

        dates_range = [
            '&dstFreeAirport=&depdate=25.1.2019&arrdate=31.5.2019',
            '&dstFreeAirport=&depdate=1.6.2019&arrdate=31.10.2019'
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


    present_timestamp = datetime.now().strftime("%d.%B.%Y %I:%M%p").split(' ')[0]
    present_day = datetime.now().strftime("%A %d.%B.%Y.%I:%M%p").split(' ')[0]

    logging.INFO('Processing' + response.url + '...')


    def process_links(self):

    def parse(self, response):
        SET_SELECTOR = '.result '

        for flight_info_box in response.css(SET_SELECTOR):
            DEPT_AER_CODE = '.code ::text'   # '.code ::text' 2x
            ARR_AER_CODE = '/html[1]/body[1]/div[5]/div[1]/div[1]/p[1]/span[4]/span[1]/text()'
            DEPT_DATE = '.date ::text'    # st\xa029.05.2019
            DEPT_TIME = '.from ::text'
            AIRLINES = '.airline ::text'
            ARR_TIME = '.to ::text'    # 20:55 Faro[mezera]
            DURATION = '.durcha ::text'    # 6:50 h / 1 p5estup
            WHOLE_PRICE = '.subPrice ::text'    # 1201 K4
            PRICE_FOR_SEPARATE_FLIGHT = '.legPrice ::text'
            SEATS_FOR_GIVEN_PRICE = '.icoSeatWrapper ::text'    # 6[mezery:       ]

            yield {
                'date of departure': flight_info_box.css(DEPT_DATE).extract_first(),
                'departure airport': flight_info_box.css(DEPT_AER_CODE).extract_first(),
                'time of departure': flight_info_box.css(DEPT_TIME).extract_first(),
                'arrival airport': flight_info_box.xpath(ARR_AER_CODE).extract_first(),
                'time of arrival': flight_info_box.css(ARR_TIME).extract_first(),
                'flight duration': flight_info_box.css(DURATION).extract_first(),
                'flight fare': flight_info_box.css(WHOLE_PRICE).extract_first(),

                'departure airport (flight 1)': flight_info_box.css(DEPT_AER_CODE).extract()[2],
                'time of departure (flight 1)': flight_info_box.css(DEPT_TIME).extract()[0], # 1
                'arrival airport (flight 1)': flight_info_box.css(DEPT_AER_CODE).extract()[3],
                'time of arrival (flight 1)': flight_info_box.css(ARR_TIME).extract()[2],
                'airlines (flight 1)': flight_info_box.css(AIRLINES).extract_first,    # check
                'flight fare (flight 1)': flight_info_box.css(PRICE_FOR_SEPARATE_FLIGHT).extract()[0],
                'seats for lower price (flight 1)': flight_info_box.css(SEATS_FOR_GIVEN_PRICE).extract_first(),

                'departure airport (flight 2)': flight_info_box.css(DEPT_AER_CODE).extract()[3],
                'time of departure (flight 2)': flight_info_box.css(DEPT_TIME).extract()[3],  # 1 PRG i u 2 PRG
                'arrival airport (flight 2)': flight_info_box.xpath(ARR_AER_CODE).extract_first(),
                'time of arrival (flight 2)': flight_info_box.css(ARR_TIME).extract_first(),
                'airlines (flight 2)': flight_info_box.css(AIRLINES).extract()[1],    # check
                'flight fare (flight 2)': flight_info_box.css(PRICE_FOR_SEPARATE_FLIGHT).extract()[1],
                'seats for lower price (flight 2)': flight_info_box.css(SEATS_FOR_GIVEN_PRICE).extract()[1],
            }

            # create a dictionary to store the scraped info
            #scraped_info = {
            #    'title': item[0],
            #    'vote': item[1],
            #    'created_at': item[2],
            #    'comments': item[3],
            #}

    def create_database(self):
        conn = sqlite3.connect('flights.db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE Flights('
                    'Date of download NUMERIC, '
                    'Date of departure NUMERIC, '
                    'Departure airport TEXT, '
                    'Departure time NUMERIC, '
                    'Arrival airport TEXT, '
                    'Arrival time NUMERIC, '
                    'Airlines TEXT'
                    'Fare TEXT'
                    'Currency TEXT'
                    'Seats for lower price TEXT')
        # cur.execute('INSERT INTO Flights (Date of departure,Departure airport,...) VALUES (a, 'c', ...)
        cur.execute('INSERT INTO Flights VALUES('24.1.2019', 'druhe')

        cur.execute('SELECT * FROM Flights')

        rows = cur.fetchall()

        for row in rows:
            print(row)

        cur.close()
        conn.commit()
        conn.close()
