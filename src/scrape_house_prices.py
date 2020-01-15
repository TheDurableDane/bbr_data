#!/usr/bin/env python
import requests
import time
import sys
import pandas as pd
import database_functions as dbf


def get_subpage_results(subpage_number):
    columns_to_use = ['address',
                  'zipCode',
                  'price',
                  'soldDate',
                  'propertyType',
                  'saleType',
                  'rooms',
                  'size',
                  'buildYear',
                  'change',
                  'guid',
                  'latitude',
                  'longitude',
                  'municipalityCode',
                  'estateCode',
                  'city']

    url = 'https://api.boliga.dk/api/v2/sold/search/results?page={}&sort=date-d'.format(subpage_number + 1)
    r = requests.get(url)
    json_object = r.json()
    single_page_results = pd.DataFrame(json_object['results'])
    subresults = single_page_results[columns_to_use]

    return subresults


def store_data_in_database(database_path, data):
    table_name = 'house_price_data'
    query = '''INSERT OR IGNORE INTO {} (address, zip_code, price, sold_date, property_type, sale_type, rooms, residence_size, build_year, price_change, guid, latitude, longitude, municipality_code, estate_code, city)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''.format(table_name)
    dbf.insert_into_database(database_path, query, data)


def scrape_data(database_path):
    house_price_columns = ['address',
                       'zip_code',
                       'price',
                       'sold_date',
                       'property_type',
                       'sale_type',
                       'rooms',
                       'residence_size',
                       'build_year',
                       'price_change',
                       'guid',
                       'latitude',
                       'longitude',
                       'municipality_code',
                       'estate_code',
                       'city']

    n_subpages = 27507
    for subpage_number in range(n_subpages):
        subresults = get_subpage_results(subpage_number)
        subresults.columns = house_price_columns
        store_data_in_database(database_path, subresults)

        sys.stdout.write('{} of {}\r'.format(subpage_number + 1, n_subpages))
        sys.stdout.flush()
        time.sleep(1)


if __name__ == '__main__':
    database_path = '../data/bbr.db'
    data = scrape_data(database_path)
