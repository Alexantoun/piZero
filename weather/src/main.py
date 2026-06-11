from textwrap import indent

from weather import open_meteo_interface, WeatherAPIError
import json
from epd_display import display
import time
from datetime import datetime
from pathlib import Path

daily_path = Path(__file__).parent.parent / 'assets' / 'files' / 'daily.json'
hourly_path = Path(__file__).parent.parent / 'assets' / 'files' / 'hourly.json'

def get_daily_data_offset(daily_data):
    """Return how many days the first cached forecast date is behind today's date."""
    first_date_str = daily_data["sunrise"][0].split('T')[0]
    first_date = datetime.strptime(first_date_str, "%Y-%m-%d").date()
    today = datetime.now().date()
    return (today - first_date).days

def extractNextDayForecast(daily_data):
    """Extract the next day's forecast from the daily data dictionary."""
    next_day_forecast = {}
    offset = get_daily_data_offset(daily_data)
    if offset > 0:
        print(f"using cached day {offset}")

    for key in daily_data:
        next_day_forecast[key] = daily_data[key][offset]
    
    print(f'Extracted next Day forecast\n{json.dumps(next_day_forecast, indent=2)}')
    return next_day_forecast


if __name__ == '__main__':
    print(f'Starting weather display program: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
    
    daily_data = None    
    if daily_path.exists():
        print(f'Reading weather data from {daily_path}')
        with open(daily_path, 'r') as daily_file:
            daily_data = json.load(daily_file)
            
            print(f'Cached  date: {daily_data["sunrise"][0].split("T")[0]}')
            print(f'Current date: {time.strftime("%Y-%m-%d", time.localtime())}')

        print(f'Daily JSON loaded successfully. Cached data:\n{json.dumps(daily_data, indent=2)}')

    print('Getting weather data from Open Meteo API')
    successful_open_meto_connection: bool
    try:
        weather = open_meteo_interface()
        print('Writing weather data to file')
        weather.write_hourly_forecast_to_file(filename=hourly_path)
        weather.write_daily_forecast_to_file(filename=daily_path)
        successful_open_meto_connection = True
    except WeatherAPIError as exc:
        print(f'Warning: failed to fetch weather data: {exc}')
        successful_open_meto_connection = False
        if daily_data is not None:
            print('Falling back to cached weather data')
            weather = None
        else:
            print('No cached weather data available. Cannot continue.')
            raise SystemExit(1) from exc

    print('Initializing display')
    myDisplay = display()

    print('Displaying today\'s forecast')
    forecast = weather.seven_day_forecast if weather is not None else extractNextDayForecast(daily_data)
    myDisplay.display_todays_forecast(forecast, successful_open_meto_connection)