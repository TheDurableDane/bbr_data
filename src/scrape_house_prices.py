#!/usr/bin/env python
import requests
import time
import sys
import pandas as pd
import database_functions as dbf


def scrape_data():
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
    house_price_data = pd.DataFrame(columns=columns_to_use)

    n_subpages = 27507
    for subpage_number in range(n_subpages):
        url = 'https://api.boliga.dk/api/v2/sold/search/results?page={}&sort=date-d'.format(subpage_number + 1)
        r = requests.get(url)
        json_object = r.json()
        temp_df = pd.DataFrame(json_object['results'])
        temp_df_subset = temp_df[columns_to_use]
        house_price_data = house_price_data.append(temp_df_subset, ignore_index=True, sort=False)
        sys.stdout.write('{} of {}\r'.format(subpage_number + 1, n_subpages))
        sys.stdout.flush()
        time.sleep(1)

    house_price_data.columns = house_price_columns

    return house_price_data


def store_data_in_database(database_path, data):
    table_name = 'house_price_data'
    query = '''INSERT OR IGNORE INTO {} (address, zip_code, price, sold_date, property_type, sale_type, rooms, residence_size, build_year, price_change, guid, latitude, longitude, municipality_code, estate_code, city)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''.format(table_name)
    dbf.insert_into_database(database_path, query, data)


if __name__ == '__main__':
    database_path = '../data/bbr.db'
    data = scrape_data()
    store_data_in_database(database_path, data)
