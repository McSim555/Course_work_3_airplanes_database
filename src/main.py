from src.utils import get_countries, get_airplanes_in_countries
from src.database import create_database

if __name__ == "__main__":
    get_airplanes_in_countries(get_countries())
    create_database('airplanes_in_countries')