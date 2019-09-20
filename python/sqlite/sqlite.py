import sqlite3

class db_connector:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

    def crete_table(self, table_name, params):
        self.table = table_name
        self.cursor.execute("CREATE TABLE IF NOT EXISTS {}({})".format(table_name, params))
        self.conn.commit()
    
    def insert(self, table_name, params):
        self.cursor.execute("INSERT INTO {} VALUES({})".format(table_name, params))
        self.conn.commit()
    
    def execute(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchall()

    def update(self, table_name, update_column, control_column, control_value, new_value):
        query = "UPDATE {table} SET {update_column} = '{new_value}' WHERE {control_column} = '{control_value}'".format(
            table = table_name,
            update_column = update_column,
            new_value = new_value,
            control_column = control_column,
            control_value = control_value)
        self.execute(query)

    def select(self, column, table, control_column, value):
        query = "SELECT {column} FROM {table} WHERE {control_column} = '{value}'".format(
            column = column,
            table = table,
            control_column = control_column,
            value = value)
        return self.execute(query)
    
    def select_all(self, column, table):
        query = "SELECT {column} FROM {table}".format(column,table)
        return self.execute(query)
