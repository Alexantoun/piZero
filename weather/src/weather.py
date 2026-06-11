import requests
import numpy
from datetime import datetime
from weather_codes import DESCRIPTION_TABLE
import json
from pathlib import Path


class WeatherAPIError(Exception):
    """Raised when Open Meteo requests fail or return invalid data."""
    pass


url = "https://api.open-meteo.com/v1/forecast"
ISO_FORMAT_STRING = "%Y-%m-%d"
DAILY_FORECAST_PARAMS = {
	"latitude": 41.636335,
	"longitude": -93.606671,
	"daily": ["temperature_2m_mean", "precipitation_sum", "sunrise", "sunset", "uv_index_max", "weather_code", "apparent_temperature_max"],
    "timezone": "America/Chicago"
}

HOURLY_FORECAST_PARAMS = {
    "latitude": 41.636335,
    "longitude": -93.606671,
    "hourly": ["temperature_2m", "precipitation_probability", "uv_index", "weather_code", "apparent_temperature"],
    "timezone": "America/Chicago",
    "start_date": datetime.now().strftime(ISO_FORMAT_STRING),
    "end_date": datetime.now().strftime(ISO_FORMAT_STRING)
}

class open_meteo_interface():
    def __init__(self):
        self._daily_forecast = {}
        raw = self._fetch_json({**DAILY_FORECAST_PARAMS, "format": "json"})
        self._daily_forecast["temperature_2m_mean"] = raw["daily"]["temperature_2m_mean"]
        self._daily_forecast["precipitation_sum"] = raw["daily"]["precipitation_sum"]
        self._daily_forecast["uv_index_max"] = raw["daily"]["uv_index_max"]
        self._daily_forecast["sunrise"] = raw["daily"]["sunrise"]
        self._daily_forecast["sunset"] = raw["daily"]["sunset"]
        self._daily_forecast["weather_code"] = raw["daily"]["weather_code"]
        self._daily_forecast["apparent_temperature_max"] = raw["daily"]["apparent_temperature_max"]

        raw = self._fetch_json({**HOURLY_FORECAST_PARAMS, "format": "json"})
        self._hourly_forecast = {}
        self._hourly_forecast["temperature_2m"] = raw["hourly"]["temperature_2m"]
        self._hourly_forecast["precipitation_probability"] = raw["hourly"]["precipitation_probability"]
        self._hourly_forecast["uv_index"] = raw["hourly"]["uv_index"]
        self._hourly_forecast["weather_code"] = raw["hourly"]["weather_code"]
        self._hourly_forecast["apparent_temperature"] = raw["hourly"]["apparent_temperature"]
        self._hourly_forecast["time"] = raw["hourly"]["time"]

    def _fetch_json(self, params):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            raw = response.json()
        except requests.RequestException as exc:
            raise WeatherAPIError("Open Meteo API request failed") from exc
        except ValueError as exc:
            raise WeatherAPIError("Open Meteo API returned invalid JSON") from exc

        if not isinstance(raw, dict):
            raise WeatherAPIError("Open Meteo API response was not a JSON object")

        return raw
        
        
    @property
    def seven_day_forecast(self):
        # return the populated daily forecast dictionary
        return self._daily_forecast
    
    def daily_weather_description(self, day):
        _weather_code = self._daily_forecast["weather_code"][day]
        return DESCRIPTION_TABLE[_weather_code]
    
    @property
    def hourly_forecast(self):
        # return the populated hourly forecast dictionary
        return self._hourly_forecast
    
    def write_hourly_forecast_to_file(self, filename=None):
        """Write hourly forecast to filename or to default hourly_path."""
        target = Path(filename) if filename else hourly_path
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, 'w') as f:
            json.dump(self._hourly_forecast, f, indent=2)

    def write_daily_forecast_to_file(self, filename=None):
        """Write daily forecast to filename or to default daily_path."""
        target = Path(filename) if filename else daily_path
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, 'w') as f:
            json.dump(self._daily_forecast, f, indent=2)
