import sqlite3


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
