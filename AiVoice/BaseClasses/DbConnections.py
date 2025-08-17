from django.db import connections


def get_data_from_db(DB, query):
    cursor = connections[DB].cursor()
    cursor.execute(query)
    row = cursor.fetchall()
    return row


def get_data_from_db_with_columns(query, DB="user_management"):
    cursor = connections[DB].cursor()
    cursor.execute(query)
    col_names = [desc for desc in cursor.description]
    row = cursor.fetchall()
    return col_names, row


def get_cursor(DB):
    return connections[DB].cursor()
