import enum
import psycopg2
import datetime

conn = psycopg2.connect(dbname="axl3210", user="axl3210", password="just@send@it!", host="reddwarf.cs.rit.edu", port="5432")
cursor = conn.cursor()
cursor.execute("SET search_path TO dataFest2018;")

def close():
    cursor.close()
    conn.commit()
    if conn is not None:
        conn.close()


# Undo because db threw an error
def undo():
    conn.rollback()
    cursor.execute("SET search_path TO packages;")


# Error handling
def error_out():
    clear()
    print("Invalid selection")