from weather import open_meteo_interface
import json
from epd_display import display
import time
from pathlib import Path

daily_path = Path(__file__).parent.parent / 'assets' / 'files' / 'daily.json'
hourly_path = Path(__file__).parent.parent / 'assets' / 'files' / 'hourly.json'


if __name__ == '__main__':
    print('Starting weather display program')

    print('Initializing display')
    myDisplay = display()
    
    _can_load_data = False
    if daily_path.exists():
        print(f'Reading weather data from {daily_path}')
        with open(daily_path, 'r') as daily_file:
            daily_data = json.load(daily_file)
            _can_load_data = daily_data["sunrise"][0].split('T')[0] == time.strftime("%Y-%m-%d", time.localtime())
            print(f'Cached  date: {daily_data["sunrise"][0].split("T")[0]}')
            print(f'Current date: {time.strftime("%Y-%m-%d", time.localtime())}')

        print('Daily JSON loaded successfully')

    if not _can_load_data:
        print('Daily weather data is not up to date. Fetching new data from Open Meteo API')
        print('Getting weather data from Open Meteo API')
        weather = open_meteo_interface()

        print('Writing weather data to file')
        weather.write_hourly_forecast_to_file(filename=hourly_path)
        weather.write_daily_forecast_to_file(filename=daily_path)
    else:
        print('Daily weather data is up to date. Using cached data')
        weather = None
    
    print('Displaying today\'s forecast')
    forecast = weather.seven_day_forecast if weather is not None else daily_data
    myDisplay.display_todays_forecast(forecast)
