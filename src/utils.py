import requests


def get_countries() -> str:
    countries = input('Введите список стран через запятую и пробел на английском языке: ').lower()
    return countries

def get_airplanes_in_countries(countries) -> list:

    countries_airplanes = countries.split(", ")
    aeroplanes_list = []

    for country in countries_airplanes:

        openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        headers_nominatim = {"User-Agent": "test-app/1.0"}
        params_nominatim = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        response = requests.get(url=openstreetmap_url, params=params_nominatim, headers=headers_nominatim)

        data = response.json()
        country_sky = data[0].get("boundingbox")

        opensky_url = "https://opensky-network.org/api/states/all?"

        params = {
            "lamin": country_sky[0],
            "lamax": country_sky[1],
            "lomin": country_sky[2],
            "lomax": country_sky[3]
        }

        response = requests.get(url=opensky_url, params=params)

        aeroplanes = response.json()
        aeroplanes_list.append(aeroplanes)

    return aeroplanes_list
