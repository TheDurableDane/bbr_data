#!/usr/bin/env python
import sqlite3
import database_functions as dbf


def initialize_database_table(database_path):
    table_name = 'house_price_data'
    query = 'CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT,\
                              address TEXT NOT NULL,\
                              zip_code INTEGER NOT NULL,\
                              price BIGINT NOT NULL,\
                              sold_date DATETIME NOT NULL,\
                              property_type INTEGER,\
                              sale_type TEXT,\
                              rooms INTEGER,\
                              residence_size INTERGER,\
                              build_year integer,\
                              price_change REAL,\
                              guid TEXT,\
                              latitude REAL,\
                              longitude REAL,\
                              municipality_code INTEGER,\
                              estate_code INTEGER,\
                              city TEXT,\
                              UNIQUE(address, zip_code, sold_date));'.format(table_name)
    dbf.execute_database_query(database_path, query)


if __name__ == '__main__':
    database_path = '../data/bbr.db'
    initialize_database_table(database_path)
