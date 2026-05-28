import requests
from requests import HTTPError, Timeout, RequestException


def get_countries() -> list[str] | None:
    i = 0
    while i < 1:
        countries = input('Введите список стран через запятую и пробел на английском языке: ').upper()
        countries_airplanes = countries.split(", ")
        for country in countries_airplanes:
            if country != '' and country.isalpha():
                i += 1
            else:
                print('Повторите ввод.')
        return countries_airplanes

def get_countries_data(countries_airplanes) -> list | None:

    countries_data = []
    for country in countries_airplanes:
        try:
            openstreetmap_url = "https://nominatim.openstreetmap.org/search"
            headers_nominatim = {"User-Agent": "test-app/1.0"}
            params_nominatim = {
                "country": country,
                "format": "json",
                "limit": 1,
            }

            response = requests.get(url=openstreetmap_url, params=params_nominatim, headers=headers_nominatim, timeout=10)

            data = response.json()
            if not data:
                print('Страны не найдены, попробуйте ввести другие на английском языке')

            else:
                country_sky = data[0]
                country_sky['name'] = country
                countries_data.append(country_sky)

        except HTTPError as e:
            print(f"HTTP-ошибка: {e.response.status_code}")
            if e.response.status_code == 404:
                print("Ресурс не найден")
                return None
            elif e.response.status_code == 500:
                print("Ошибка сервера")
                return None
        except ConnectionError:
            print("Ошибка подключения: проверьте интернет или доступность API")
            return None
        except Timeout:
            print("Превышено время ожидания ответа от сервера")
            return None
        except requests.JSONDecodeError:
            print("Ответ не в формате JSON")
            return None
        except RequestException as e:
            print(f"Общая ошибка запроса: {e}")
            return None
    return countries_data


def get_airplanes_in_countries(country_coordinates):

    aeroplanes_by_country = []

    for country in country_coordinates:
        opensky_url = "https://opensky-network.org/api/states/all?"
        params = {
            "lamin": country.get("boundingbox")[0],
            "lamax": country.get("boundingbox")[1],
            "lomin": country.get("boundingbox")[2],
            "lomax": country.get("boundingbox")[3]
        }

        try:
            response = requests.get(url=opensky_url, params=params, timeout=10)
            airplanes = response.json()
            aeroplanes_list = []

            for airplane in airplanes['states']:
                aeroplanes_short = {
                        "ID": airplane[0],
                        "call_sign": airplane[1],
                        "registration_country": airplane[2],
                        "ground_speed": airplane[9],
                        "altitude": airplane[-4],
                        "on_ground_status": airplane[8]
                    }

                aeroplanes_list.append(aeroplanes_short)

        except HTTPError as e:
            print(f"HTTP-ошибка: {e.response.status_code}")
            if e.response.status_code == 404:
                print("Ресурс не найден")
                return None
            elif e.response.status_code == 500:
                print("Ошибка сервера")
                return None
        except ConnectionError:
            print("Ошибка подключения: проверьте интернет или доступность API")
            return None
        except Timeout:
            print("Превышено время ожидания ответа от сервера")
            return None
        except requests.JSONDecodeError:
            print("Ответ не в формате JSON")
            return None
        except RequestException as e:
            print(f"Общая ошибка запроса: {e}")
            return None

        aeroplanes_by_country_dict = dict(country=country, airplanes=aeroplanes_list)
        aeroplanes_by_country.append(aeroplanes_by_country_dict)
        aeroplanes_by_country_dict = {}

    return aeroplanes_by_country
