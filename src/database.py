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
                country_name VARCHAR(100) NOT NULL
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE airplanes (
                airplane_id serial PRIMARY KEY,
                airplane_number VARCHAR(25) NOT NULL,
                country_id int NOT NULL,
                FOREIGN KEY (country_id) REFERENCES countries(country_id),      
                callsign VARCHAR(10),
                registration_country VARCHAR(50) NOT NULL,
                ground_speed int,
                altitude int,
                on_ground_status boolean NOT NULL
            )
        """)

    conn.commit()
    conn.close()


def fill_database(data: list[dict], database_name: str):
    """Сохранение данных о самолётах в базу данных."""

    conn = psycopg2.connect(dbname=database_name, host=os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'), port=os.getenv('port'))

    with conn.cursor() as cur:
        for data_set in data:
            cur.execute(
                """
                INSERT INTO countries (country_name)
                VALUES (%s)
                RETURNING country_id
                """,
                (data_set['country'],)
            )
            country_id = cur.fetchone()[0]
            airplanes_data = data_set['airplanes']
            for value in airplanes_data:
                cur.execute(
                    """
                    INSERT INTO airplanes (airplane_number, country_id, callsign, registration_country, ground_speed, altitude, on_ground_status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (value['ID'], country_id, value['call_sign'], value['registration_country'], value['ground_speed'], value['altitude'], value['on_ground_status'])
                )

    conn.commit()
    conn.close()