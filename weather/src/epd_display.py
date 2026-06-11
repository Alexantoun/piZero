#!/usr/bin/python
# -*- coding:utf-8 -*-
from lafvin_epd import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path

from weather_codes import DESCRIPTION_TABLE

icons_path = Path(__file__).parent.parent / 'assets' / 'icons'
font15 = ImageFont.truetype(Path(__file__).parent.parent / 'assets' / 'fonts' / 'Font.ttc', 15)

ICONS_SIZE = 50

class display:
    def __init__(self):
        self.epd = epd2in13_V4.EPD()
        self.clear_display()
        

    def display_todays_forecast(self, forecast: dict, connection_successful: bool):
        _image = Image.new('1', (self.epd.height, self.epd.width), 255)
        
        _weather_code_data = forecast["weather_code"][0]
        _wc_description, _wc_icon = DESCRIPTION_TABLE[_weather_code_data]
        
        print(f"Today's weather code is {_weather_code_data} which means {_wc_description} and has the icon {_wc_icon}")

        #paste weather code icon
        bmp = Image.open(icons_path / _wc_icon)
        _image.paste(bmp, (5,0))

        _text_vert_offset = 0
        _text_horiz_offset = ICONS_SIZE + 15
        _draw = ImageDraw.Draw(_image)
        
        _draw.text((_text_horiz_offset, _text_vert_offset), f"Weather: {_wc_description}", font = font15, fill = 0)
        
        _text_vert_offset += 20
        _draw.text((_text_horiz_offset, _text_vert_offset), f"Temp: {forecast['temperature_2m_mean'][0]}°C", font = font15, fill = 0)
        
        _text_vert_offset += 20
        _draw.text((_text_horiz_offset, _text_vert_offset), f"UV Index: {forecast['uv_index_max'][0]}", font = font15, fill = 0)

        _text_vert_offset += 20
        _draw.text((_text_horiz_offset, _text_vert_offset), f"Feels Like: {forecast['apparent_temperature_max'][0]}°C", font = font15, fill = 0)
                
        _text_vert_offset += 20
        _draw.text((_text_horiz_offset, _text_vert_offset), f"Precipitation: {forecast['precipitation_sum'][0]}mm", font = font15, fill = 0)

        _text_vert_offset += 20
        _draw.text((_text_horiz_offset, _text_vert_offset), f"Sunset: {forecast['sunset'][0].split('T')[1][:5]}", font = font15, fill = 0)

        #draw date under weather code icon
        _text_ver_offset = ICONS_SIZE + 15
        _text_horiz_offset = 10
        _today = time.strftime("%d/%m", time.localtime())
        _draw.text((_text_horiz_offset, _text_ver_offset), f"{_today}", font = font15, fill = 0)

        if not connection_successful:
            #draw failed connect under date
            bmp = Image.open(icons_path / 'no_internet.bmp')
            bmp = bmp.resize((30, 30))
            _image.paste(bmp, (15, _text_ver_offset + 25))

        print('Displaying image on screen')
        print('\tTodays Date: ' + _today)
        print(f"\tWeather Code: {_weather_code_data} - {_wc_description}"
            + f"\n\tTemperature: {forecast['temperature_2m_mean'][0]}°C"
            + f"\n\tUV Index: {forecast['uv_index_max'][0]}"
            + f"\n\tFeels Like: {forecast['apparent_temperature_max'][0]}°C"
            + f"\n\tPrecipitation: {forecast['precipitation_sum'][0]}mm"
            + f"\n\tSunset: {forecast['sunset'][0].split('T')[1][:5]}"
        )

        self.epd.display(self.epd.getbuffer(_image))

        print('Putting display to sleep')
        self.epd.sleep()

    def clear_display(self):
        self.epd.init()
        self.epd.Clear(0xFF)

