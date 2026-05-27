from src.utils import get_countries, get_airplanes_in_countries
from src.database import create_database, fill_database

if __name__ == "__main__":

    create_database('airplanes_in_countries')
    # c = get_countries()
    # a = get_airplanes_in_countries(c)

    fill_database(get_airplanes_in_countries(get_countries()), 'airplanes_in_countries')