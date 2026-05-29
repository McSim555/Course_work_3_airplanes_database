from unittest.mock import Mock, patch

import requests
from requests import HTTPError, RequestException

from src.utils import get_airplanes_in_countries, get_countries, get_countries_data


def test_all_countries_alpha():
    with patch("builtins.input", return_value="France, Germany, Italy"):
        result = get_countries()
    assert result == ["FRANCE", "GERMANY", "ITALY"]


def test_et_countries_data():
    mock_response = Mock()
    mock_response.json.return_value = [{"place_id": 123, "lat": "55.75", "lon": "37.62", "display_name": "Russia"}]
    with patch("src.utils.requests.get", return_value=mock_response) as mock_get:
        result = get_countries_data(["RUSSIA"])

        mock_get.assert_called_once()
        assert len(result) == 1
        assert result[0]["name"] == "RUSSIA"
        assert result[0]["lat"] == "55.75"


def mock_success_response(*args, **kwargs):
    mock_resp = Mock()
    mock_resp.json.return_value = {
        "states": [
            ["abc123", "AFL123", "Russia", None, None, None, None, None, False, 250.5, None, 10000, None, None, 10000]
        ]
    }
    return mock_resp


def test_successful_airplanes_fetch():
    sample_countries = [
        {"name": "Russia", "boundingbox": ["55.0", "56.0", "37.0", "38.0"]},
        {"name": "France", "boundingbox": ["42.0", "43.0", "-1.0", "0.0"]},
    ]
    with patch("src.utils.requests.get", side_effect=mock_success_response) as mock_get:
        result = get_airplanes_in_countries(sample_countries)

        assert mock_get.call_count == len(sample_countries)
        assert len(result) == 2
        assert result[0]["country"] == sample_countries[0]
        assert len(result[0]["airplanes"]) == 1
        airplane = result[0]["airplanes"][0]
        assert airplane["ID"] == "abc123"
        assert airplane["call_sign"] == "AFL123"
        assert airplane["registration_country"] == "Russia"
        assert airplane["ground_speed"] == 250.5
        assert airplane["altitude"] == 10000
        assert airplane["on_ground_status"] is False


def test_empty_api_response():
    sample_countries = [
        {"name": "Russia", "boundingbox": ["55.0", "56.0", "37.0", "38.0"]},
        {"name": "France", "boundingbox": ["42.0", "43.0", "-1.0", "0.0"]},
    ]
    mock_resp = Mock()
    mock_resp.json.return_value = {"states": []}

    with patch("src.utils.requests.get", return_value=mock_resp):
        result = get_airplanes_in_countries([sample_countries[0]])

        assert len(result) == 1
        assert result[0]["airplanes"] == []


def test_general_request_exception():
    sample_countries = [
        {"name": "Russia", "boundingbox": ["55.0", "56.0", "37.0", "38.0"]},
        {"name": "France", "boundingbox": ["42.0", "43.0", "-1.0", "0.0"]},
    ]
    with patch("src.utils.requests.get", side_effect=RequestException("Network error")):
        result = get_airplanes_in_countries(sample_countries)
        assert result is None


def test_connection_error():
    sample_countries = [
        {"name": "Russia", "boundingbox": ["55.0", "56.0", "37.0", "38.0"]},
        {"name": "France", "boundingbox": ["42.0", "43.0", "-1.0", "0.0"]},
    ]
    with patch("src.utils.requests.get", side_effect=ConnectionError):
        result = get_airplanes_in_countries(sample_countries)
        assert result is None


def test_http_404_error():
    sample_countries = [
        {"name": "Russia", "boundingbox": ["55.0", "56.0", "37.0", "38.0"]},
        {"name": "France", "boundingbox": ["42.0", "43.0", "-1.0", "0.0"]},
    ]
    error_resp = Mock()
    error_resp.status_code = 404
    error = HTTPError(response=error_resp)

    with patch("src.utils.requests.get", side_effect=error):
        result = get_airplanes_in_countries(sample_countries)
        assert result is None


def test_get_countries_data_connection_error():
    with patch("src.utils.requests.get", side_effect=ConnectionError):
        result = get_countries_data(["Russia"])
        assert result is None


def test_get_countries_data_json_decode_error():
    mock_resp = Mock()
    mock_resp.json.side_effect = requests.JSONDecodeError("Invalid JSON", "", 0)

    with patch("src.utils.requests.get", return_value=mock_resp):
        result = get_countries_data(["Russia"])
        assert result is None
