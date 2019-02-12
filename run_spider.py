#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from scraper import run_spider, edit_data
from database import create_database, import_to_database
from charts import create_charts

output_csv = run_spider()
formatted_output = edit_data(path_to_data=output_csv)

if os.path.exists('flights.db') is False:
    create_database()
import_to_database(path_to_data=formatted_output)
os.rename(formatted_output, f'imported_files/{formatted_output}')

export_command = input('Would you like to export charts? [y/n] ')
while export_command != 'y' and export_command != 'n':
    print('Didn\'t understand your answer.')
    export_command = input('Please answer again: ')
if export_command == 'y':
    create_charts()
    print('Charts successfully created.')
elif export_command == 'n':
    print('Program will now quit.')
