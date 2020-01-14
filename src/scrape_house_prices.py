import requests
import time
import pandas as pd

"""
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
"""
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

n_subpages = 2
for subpage_number in range(n_subpages):
    url = 'https://api.boliga.dk/api/v2/sold/search/results?page={}&sort=date-d'.format(subpage_number + 1)
    r = requests.get(url)
    json_object = r.json()
    temp_df = pd.DataFrame(json_object['results'])
    temp_df_subset = temp_df[columns_to_use]
    
    house_price_data = house_price_data.append(temp_df, ignore_index=True, sort=False)

    time.sleep(1)
