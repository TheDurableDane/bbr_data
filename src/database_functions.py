import sqlite3
import pandas as pd


def connect_to_database(path):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    return connection, cursor


def disconnect_from_database(connection):
    connection.commit()
    connection.close()


def execute_database_query(database_path, query):
    connection, cursor = connect_to_database(database_path)
    cursor.execute(query)
    disconnect_from_database(connection)


def insert_into_database(database_path, query, data):
    connection, cursor = connect_to_database(database_path)
    cursor.executemany(query, data.values)
    disconnect_from_database(connection)


def select_from_database(database_path, query):
    connection, cursor = connect_to_database(database_path)
    cursor.execute(query)
    data = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    disconnect_from_database(connection)
    data = pd.DataFrame(data=data, columns=column_names)

    return data


def read_house_price_data(database_path):
    query = 'SELECT * FROM house_price_data;'
    house_price_data = select_from_database(database_path, query)

    return house_price_data
