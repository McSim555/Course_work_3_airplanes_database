from src.database import create_database, fill_database
from src.db_manager import DBManager
from src.utils import get_airplanes_in_countries, get_countries, get_countries_data

if __name__ == "__main__":

    create_database("airplanes_in_countries")

    fill_database(get_airplanes_in_countries(get_countries_data(get_countries())), "airplanes_in_countries")

    db = DBManager("airplanes_in_countries", "../.env")
    result_1 = db.get_countries_and_aeroplanes_count()
    print(f"Список стран с количеством самолётов в их воздушном пространстве: {result_1}")

    result_2 = db.get_all_aeroplanes()
    print(f"Список всех самолётов: {result_2}")

    result_3 = db.get_avg_speed()
    print(f"Средняя скорость всех самолётов: {result_3}")

    result_4 = db.get_aeroplanes_with_higher_speed()
    print(f"Список всех самолётов, у которых скорость выше средней: {result_4}")

    result_5 = db.get_aeroplanes_with_keyword("ACA")
    print(f"Список всех самолётов, у которых в позывном содержатся переданные в метод символы: {result_5}")

    # print(get_airplanes_in_countries(get_countries_data(get_countries())))
