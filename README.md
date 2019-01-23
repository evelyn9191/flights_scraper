# Flights Scraper
Website scraper for working with data on flights.

## Main flow
1. Scrapes website for data on flights on chosen routes. In this case from Prague to Faro,
Reykjavik, Tromso, Dublin, Nice, Japan, and back including routes from Lisabon, Porto 
and Oslo.
2. Stores data to mySQL database.
3. Puts data to charts.
4. Prints information on when to buy the cheapest flights based on the data.
5. Uses Flask to integrate charts and data to a website.

Nice to have:

3a. Compares data with last year data and draws conclusions.

### Current state of the project
As of 24th January 2019: working on point 1