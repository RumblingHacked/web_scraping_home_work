import sys
import urllib
import parser
from bs4 import BeautifulSoup
from datetime import datetime
from requests import request
import csv


entries = []

def wagner_noel():

    venue_url = 'https://www.wagnernoel.com/events'
    venue_url_root = 'https://www.wagnernoel.com/'
    venue = 'wagnernoel'
    venue_address = '1310 N. FM 1788'
    venue_city = 'Midland'
    venue_default_price = -1
    price = venue_default_price
    try:
        soup = BeautifulSoup(urllib.request.urlopen(
            urllib.request.Request(
                venue_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
                    'Accept-Language': 'en-US,en;q=0.5',
                })).read(), 'html.parser')
        # parse soup for dates
        for event in soup.find_all('div', class_='eventItem'):
            date = event.find('div', class_='date').text.strip()
            try:
                event_url = event.find('h3', class_='title').a['href']
                event_soup = BeautifulSoup(urllib.request.urlopen(
            urllib.request.Request(
                event_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
                    'Accept-Language': 'en-US,en;q=0.5',
                })).read(), 'html.parser')

                name = event.find('h3', class_='title').text.strip()
                description = event_soup.find('div', class_='event_description').text.strip()
                time = event_soup.find('li', class_='item').findNext('li', class_='item').span.text.strip()
                picture = event.find('div', class_='thumb').img['src']
                price = event_soup.find('li', class_='item itelong').text.strip()

                entries.append({

                   "name": name,
                   "venue": venue,
                   "venue_address": venue_address,
                   "date": date,
                   "time": time,
                   "venue_city": venue_city,
                   "event_url": event_url,
                   "description": description,
                   "picture": picture,
                   "price": price,

                })
            except:
                print(sys.exc_info())
        print(entries)
    except:
        print("ERROR: Failed to retrieve calendar: "+venue_url)
        print(sys.exc_info())
    write_file()

def write_file():
    csv_file = open('WagnerEvents.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['name', 'venue', 'venue_address', 'date', 'time', 'venue_city', 'event_url', 'description','picture', 'price'])
    for row in entries:
        csv_writer.writerow([row['name'], row['venue'], row['venue_address'], row['date'], row['time'], row['venue_city'], row['event_url'], row['description'], row['picture'], row['price']])
    csv_file.close()

wagner_noel()