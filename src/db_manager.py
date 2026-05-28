import psycopg2
import os

from dotenv import load_dotenv

class DBManager:
    def __init__(self, db_name: str, path_to_env: str) -> None:
        self.db_name = db_name
        self.path = path_to_env

    def connect(self):
        load_dotenv(self.path)
        conn = psycopg2.connect(dbname=self.db_name, host=os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'), port=os.getenv('port'))
        conn.autocommit = True
        return conn

    def get_countries_and_aeroplanes_count(self) -> list:
        conn = self.connect()
        countries_list = []
        with conn.cursor() as cur:
            cur.execute("""
            SELECT countries.country_id,countries.country_name, COUNT(airplanes.airplane_id) AS airplane_count
            FROM airplanes
            LEFT JOIN countries USING (country_id)
            GROUP BY countries.country_id, countries.country_name;
            """)
            rows = cur.fetchall()
            for row in rows:
                data_dict = {row[1]: row[2]}
                countries_list.append(data_dict)
        conn.close()
        return countries_list


    def get_all_aeroplanes(self):
        conn = self.connect()
        airplanes_list = []
        with conn.cursor() as cur:
            cur.execute("""
                    SELECT airplane_id, callsign, registration_country 
                    FROM airplanes;
                    """)
            column_names = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            for row in rows:
                data_dict = {
                    column_names[0]: row[0],
                    column_names[1]: row[1],
                    column_names[2]: row[2]
                }
                airplanes_list.append(data_dict)
        conn.close()
        return airplanes_list


    def get_avg_speed(self):
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute("""
                            SELECT ROUND(AVG(ground_speed),2) 
                            AS avg_speed 
                            FROM airplanes;
                            """)
            result = cur.fetchone()[0]

        conn.close()

        return result


    def get_aeroplanes_with_higher_speed(self):
        conn = self.connect()
        airplanes_list = []
        with conn.cursor() as cur:
            cur.execute("""
                    SELECT * FROM airplanes 
                    WHERE ground_speed > (SELECT AVG(ground_speed) FROM airplanes);
                    """)
            column_names = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            for row in rows:
                data_dict = {
                    column_names[0]: row[0],
                    column_names[1]: row[1],
                    column_names[2]: row[2],
                    column_names[5]: row[5]
                }
                airplanes_list.append(data_dict)
        conn.close()
        return airplanes_list


    def get_aeroplanes_with_keyword(self, keyword: str):
        conn = self.connect()
        airplanes_list = []
        with conn.cursor() as cur:
            cur.execute(
        "SELECT * FROM airplanes WHERE callsign LIKE %s",
            (f"%{keyword}%",)
                        )
            column_names = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            for row in rows:
                data_dict = {
                    column_names[0]: row[0],
                    column_names[1]: row[1],
                    column_names[2]: row[2],
                    column_names[3]: row[3]
                }
                airplanes_list.append(data_dict)
        conn.close()
        return airplanes_list
