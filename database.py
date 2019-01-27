import sqlite3


DB_NAME = 'flights.db'
DB_CONNECTION = sqlite3.connect(DB_NAME)
DB_CURSOR = DB_CONNECTION.cursor()


def create_database():
    """Create database if it doesn't exist yet."""
    DB_CONNECTION.execute('''CREATE TABLE IF NOT EXISTS Flights (
                uid int,
                date_of_departure numeric,
                departure_airport text,
                time_of_departure numeric,
                arrival_airport text,
                time_of_arrival numeric,
                flight_duration text,
                flight_fare int,
                departure_airport_flight_1 text,
                time_of_departure_flight_1 numeric,
                arrival_airport_flight_1 text,
                time_of_arrival_flight_1 numeric,
                airlines_flight_1 text,
                flight_fare_flight_1 int,
                seats_for_lower_price_flight_1 int,
                departure_airport_flight_2 text,
                time_of_departure_flight_2 numeric,
                arrival_airport_flight_2 text,
                time_of_arrival_flight_2 numeric,
                airlines_flight_2 text,
                flight_fare_flight_2 int,
                seats_for_lower_price_flight_2 int,
                date_of_download numeric,
                day_of_download text,
                day_of_departure text)''')
    DB_CONNECTION.commit()


def import_to_database(path_to_data):
    """Import data from .csv file to database."""
    scraped_data = pd.read_csv(path_to_data, sep='|')
    scraped_data.to_sql('Flights', DB_CONNECTION, if_exists='append', index=False)
    DB_CONNECTION.commit()
