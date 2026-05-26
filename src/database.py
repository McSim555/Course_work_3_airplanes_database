import psycopg2
import os

from dotenv import load_dotenv

def create_database(database_name: str):
    """Создание базы данных и таблиц для сохранения данных о странах и самолётах."""

    load_dotenv("../.env")
    conn = psycopg2.connect(dbname='postgres', host=os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'), port=os.getenv('port'))
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()
    conn = psycopg2.connect(dbname=database_name, host=os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'), port=os.getenv('port'))

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE countries (
                country_id serial PRIMARY KEY,
                country_name VARCHAR(255) NOT NULL
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE airplanes (
                airplane_id VARCHAR(10) PRIMARY KEY,
                country_id int NOT NULL,
                FOREIGN KEY (country_id) REFERENCES countries(country_id),      
                callsign VARCHAR(10) NOT NULL,
                registration_country VARCHAR(50) NOT NULL,
                ground_speed int NOT NULL,
                altitude int NOT NULL,
                on_ground_status boolean NOT NULL
            )
        """)

    conn.commit()
    conn.close()