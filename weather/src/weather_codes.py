# Weather variable documentation
#   WMO Weather interpretation codes (WW)
#      Code	        Description
#      0	        Clear sky
#      1, 2, 3	    Mainly clear, partly cloudy, and overcast
#      45, 48	    Fog and depositing rime fog
#      51, 53, 55	Drizzle: Light, moderate, and dense intensity
#      56, 57	    Freezing Drizzle: Light and dense intensity
#      61, 63, 65	Rain: Slight, moderate and heavy intensity
#      66, 67	    Freezing Rain: Light and heavy intensity
#      71, 73, 75	Snow fall: Slight, moderate, and heavy intensity
#      77	        Snow grains
#      80, 81, 82	Rain showers: Slight, moderate, and violent
#      85, 86	    Snow showers slight and heavy
#      95 *	        Thunderstorm: Slight or moderate
#      96, 99 *	    Thunderstorm with slight and heavy hail -> not available in USA

DESCRIPTION_TABLE = {
    0: ("Clear sky", "sun.bmp"),

    1: ("Mainly clear", "partly_cloudy.bmp"),
    2: ("Partly cloudy", "partly_cloudy.bmp"),

    3: ("Overcast", "cloud.bmp"),
    45: ("Fog", "cloud.bmp"),
    48: ("Depositing rime fog", "cloud.bmp"),

    51: ("Drizzle: Light intensity", "rain.bmp"),
    53: ("Drizzle: Moderate intensity", "rain.bmp"),
    55: ("Drizzle: Dense intensity", "rain.bmp"),

    56: ("Freezing Drizzle: Light intensity", "snow.bmp"),
    57: ("Freezing Drizzle: Dense intensity", "snow.bmp"),

    61: ("Rain: Slight intensity", "rain.bmp"),
    63: ("Rain: Moderate intensity", "rain.bmp"),
    65: ("Rain: Heavy intensity", "rain.bmp"),

    66: ("Freezing Rain: Light intensity", "freeze.bmp"),
    67: ("Freezing Rain: Heavy intensity", "freeze.bmp"),

    71: ("Snow fall: Slight intensity", "snow.bmp"),
    73: ("Snow fall: Moderate intensity", "snow.bmp"),
    75: ("Snow fall: Heavy intensity", "snow.bmp"),
    77: ("Snow grains", "snow.bmp"),

    80: ("Rain showers: Slight intensity", "rain.bmp"),
    81: ("Rain showers: Moderate intensity", "rain.bmp"),
    82: ("Rain showers: Violent intensity", "rain.bmp"),

    85: ("Snow showers: Slight intensity", "snow.bmp"),
    86: ("Snow showers: Heavy intensity", "snow.bmp"),

    95: ("Thunderstorm: Slight or moderate", "thunderstorm.bmp"),
    96: ("Thunderstorm with slight hail", "thunderstorm.bmp"),
    99: ("Thunderstorm with heavy hail", "thunderstorm.bmp")
}