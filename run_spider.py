#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from scraper import run_spider, edit_data
from database import create_database, import_to_database
from charts import create_charts

print('Began scraping.')
output_csv = run_spider()
formatted_output = edit_data(path_to_data=output_csv)

if os.path.exists('flights.db') is False:
    create_database()
import_to_database(path_to_data=formatted_output)

while True:
    input = 'Would you like to also export charts? [y/n] '
    if input == 'y':
        create_charts()
        print('Charts successfully created.')
        break
    elif input == 'n':
        print('Program will now quit.')
        break
    else:
        print('Didn\'t understand your answer. Please answer again.')
