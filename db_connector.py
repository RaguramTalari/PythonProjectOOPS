import mysql.connector as sql

def get_db_connection():
    return sql.connect(
        host="localhost",
        user="root",
        password="tAlari@1",
        database="USERS"
    )
