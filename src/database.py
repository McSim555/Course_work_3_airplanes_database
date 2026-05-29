import os

import psycopg2
from dotenv import load_dotenv


def create_database(database_name: str):
    """Создание базы данных и таблиц для сохранения данных о странах и самолётах."""

    load_dotenv("../.env")
    conn = psycopg2.connect(
        dbname="postgres",
        host=os.getenv("host"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        port=os.getenv("port"),
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()
    conn = psycopg2.connect(
        dbname=database_name,
        host=os.getenv("host"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        port=os.getenv("port"),
    )

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE countries (
                country_id serial PRIMARY KEY,
                country_name VARCHAR(100) NOT NULL,
                place_id int NOT NULL,
                type VARCHAR(50) NOT NULL,
                place_rank int,
                display_name VARCHAR(50),
                osm_type VARCHAR(50),
                osm_id int NOT NULL,
                lat float,
                lon float
            );
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE airplanes (
                airplane_id serial PRIMARY KEY,
                airplane_number VARCHAR(25) NOT NULL,
                country_id int NOT NULL,FOREIGN KEY (country_id) REFERENCES countries(country_id),      
                callsign VARCHAR(10),
                registration_country VARCHAR(50) NOT NULL,
                ground_speed int,
                altitude int,
                on_ground_status boolean NOT NULL
            );
        """)

    conn.commit()
    conn.close()


def fill_database(data: list[dict], database_name: str):
    """Сохранение данных о самолётах в базу данных."""

    conn = psycopg2.connect(
        dbname=database_name,
        host=os.getenv("host"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        port=os.getenv("port"),
    )

    with conn.cursor() as cur:
        for data_set in data:
            cur.execute(
                """INSERT INTO countries 
                (country_name, place_id, type, place_rank, display_name, osm_type, osm_id, lat, lon)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING country_id
                """,
                (
                    data_set["country"]["name"],
                    data_set["country"]["place_id"],
                    data_set["country"]["type"],
                    data_set["country"]["place_rank"],
                    data_set["country"]["display_name"],
                    data_set["country"]["osm_type"],
                    data_set["country"]["osm_id"],
                    data_set["country"]["lat"],
                    data_set["country"]["lon"],
                ),
            )

            country_id = cur.fetchone()[0]

            airplanes_data = data_set["airplanes"]
            for value in airplanes_data:
                cur.execute(
                    """INSERT INTO airplanes (airplane_number, country_id, callsign, 
                    registration_country, ground_speed, altitude, 
                    on_ground_status) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (
                        value["ID"],
                        country_id,
                        value["call_sign"],
                        value["registration_country"],
                        value["ground_speed"],
                        value["altitude"],
                        value["on_ground_status"],
                    ),
                )

    conn.commit()
    conn.close()
