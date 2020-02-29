#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from datetime import datetime

from scraper.scrape_website import run_spider, edit_data
from scraper.database import create_database, import_to_database
from scraper.charts import create_charts, ROOT


def scrape_flights():
    output_csv = run_spider()
    formatted_output = edit_data(path_to_data=output_csv)

    if os.path.exists('flights.db') is False:
        create_database()
    import_to_database(path_to_data=formatted_output)

    imported_files_path = ROOT / "imported_files"
    os.rename(formatted_output, imported_files_path / formatted_output)

    dates_to_run_spider = ['01.03.2019', '15.03.2019', '01.04.2019', '15.04.2019', '01.05.2019',
                           '15.05.2019', '01.06.2019', '15.06.2019', '01.07.2019', '20.07.2019']
    TIMESTAMP = datetime.now().strftime('%d-%m-%Y')

    for date in dates_to_run_spider:
        date = datetime.strptime(date, '%d.%m.%Y').strftime('%d-%m-%Y')
        if date == TIMESTAMP:
            create_charts()


if __name__ == '__main__':
    scrape_flights()
