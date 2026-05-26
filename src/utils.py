import requests
from requests import HTTPError, Timeout, RequestException


def get_countries() -> str:
    i = 0
    while i < 1:
        countries = input('Введите список стран через запятую и пробел на английском языке: ').upper()
        if countries != '' and countries.isalpha():
            i += 1
            return countries
        else:
            print('Повторите ввод.')

def get_airplanes_in_countries(countries) -> list | None:

    countries_airplanes = countries.split(", ")
    aeroplanes_list = []

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
                break

            country_sky = data[0].get("boundingbox")

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

        opensky_url = "https://opensky-network.org/api/states/all?"
        params = {
            "lamin": country_sky[0],
            "lamax": country_sky[1],
            "lomin": country_sky[2],
            "lomax": country_sky[3]
        }

        try:
            response = requests.get(url=opensky_url, params=params, timeout=10)
            airplanes = response.json()

            for airplane in airplanes['states']:
                aeroplanes_short = {
                        "ID": airplane[0],
                        "call_sign": airplane[1],
                        "registration_country": airplane[2],
                        "ground_speed": airplane[9],
                        "altitude": airplane[-4],
                        "on_ground_status": airplane[8]
                    }

                aeroplanes_dict = {
                    'country': country,
                    'airplanes': aeroplanes_short
                }

                aeroplanes_list.append(aeroplanes_dict)
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

    return aeroplanes_list
