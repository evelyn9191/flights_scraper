# Flights Scraper
Website scraper for working with data on flights.

## Main flow
1. Scrapes website for data on flights on chosen routes. In this case from Prague to Faro,
Reykjavik, Tromso, Nice, and back including route from Lisabon.
2. Stores data to SQLite database.
3. Puts data to charts.
4. Prints information on when to buy the cheapest flights based on the data.
5. Uses Flask to integrate charts and data to a website.

Nice to have:

3a. Compares data with last year data and draws conclusions.

### Current state of the project
As of 4th February 2019: points 1 and 2 finished, working on 3 and 4.
