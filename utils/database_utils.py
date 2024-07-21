import sqlite3
from config import config

DATABASE_PATH = config["DATABASE_PATH"]

def create_table(table_name, columns):
    """Creates a table in the SQLite database.

    Args:
        table_name: The name of the table to create.
        columns: A list of tuples representing the columns, each tuple containing
            (column_name, data_type).
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        column_definitions = ", ".join(
            f"{name} {data_type}" for name, data_type in columns
        )
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})")
        conn.commit()
        conn.close()
        print(f"Table '{table_name}' created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")

def insert_data(table_name, data):
    """Inserts data into a table in the SQLite database.

    Args:
        table_name: The name of the table to insert data into.
        data: A dictionary representing the data to insert, with keys matching
            column names.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        column_names = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(data.values())
        cursor.execute(
            f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})", values
        )
        conn.commit()
        conn.close()
        print(f"Data inserted into table '{table_name}' successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")

def update_data(table_name, data, where_clause):
    """Updates data in a table in the SQLite database.

    Args:
        table_name: The name of the table to update.
        data: A dictionary representing the data to update, with keys matching
            column names.
        where_clause: A string representing the WHERE clause for the update statement.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        set_statements = ", ".join(
            f"{name} = ?" for name in data.keys()
        )
        values = tuple(data.values()) + tuple(where_clause.split("=")[-1].strip().split(","))
        cursor.execute(
            f"UPDATE {table_name} SET {set_statements} WHERE {where_clause}", values
        )
        conn.commit()
        conn.close()
        print(f"Data updated in table '{table_name}' successfully.")
    except Exception as e:
        print(f"Error updating data: {e}")

def delete_data(table_name, where_clause):
    """Deletes data from a table in the SQLite database.

    Args:
        table_name: The name of the table to delete data from.
        where_clause: A string representing the WHERE clause for the delete statement.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE {where_clause}")
        conn.commit()
        conn.close()
        print(f"Data deleted from table '{table_name}' successfully.")
    except Exception as e:
        print(f"Error deleting data: {e}")

def select_data(table_name, columns=None, where_clause=None, order_by=None):
    """Retrieves data from a table in the SQLite database.

    Args:
        table_name: The name of the table to retrieve data from.
        columns: A list of column names to retrieve, or None to retrieve all
            columns.
        where_clause: A string representing the WHERE clause for the select statement.
        order_by: A string representing the ORDER BY clause for the select statement.

    Returns:
        A list of tuples representing the retrieved data.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        query = f"SELECT "
        if columns is None:
            query += "* "
        else:
            query += ", ".join(columns) + " "
        query += f"FROM {table_name} "
        if where_clause is not None:
            query += f"WHERE {where_clause} "
        if order_by is not None:
            query += f"ORDER BY {order_by}"
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return None