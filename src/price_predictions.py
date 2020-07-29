#!/usr/bin/env python
import pandas as pd
import database_functions as dbf


def load_data(database_path):
    all_data = dbf.read_house_price_data(database_path)

    return all_data


def clean_rows(all_data):
    """
    Remove rows with data that is clearly wrong.
    """
    is_regular_sale = all_data['sale_type'] == 'Alm. Salg'
    is_reasonably_sized = all_data['residence_size'] >= 10
    is_reasonably_sized_rooms = all_data['residence_size']/all_data['rooms'] > 10
    is_sold_after_1990 = all_data['sold_date'] > pd.to_datetime('1990-01-01', format='%Y-%m-%d', utc=True)

    cleaned_data = all_data[is_regular_sale &
                            is_reasonably_sized &
                            is_reasonably_sized_rooms &
                            is_sold_after_1990]

    return cleaned_data


def clean_columns(all_data):
    """
    Remove unnecessary columns.
    """
    columns_to_keep = ['id',
                       'zip_code',
                       'price',
                       'sold_date',
                       'property_type',
                       'rooms',
                       'residence_size',
                       'build_year',
                       'latitude',
                       'longitude']
    cleaned_data = all_data[columns_to_keep]

    return cleaned_data


database_path = '../data/bbr.db'
all_data = load_data(database_path)
data = (all_data.pipe(clean_rows)
                .pipe(clean_columns))
