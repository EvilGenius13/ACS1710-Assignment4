import os
import requests

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
#from geopy.geocoders import Nominatim


################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()

pp = PrettyPrinter(indent=4)

API_KEY = os.getenv('API_KEY')
API_URL = 'http://api.openweathermap.org/data/2.5/weather'


################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""
    context = {
        'min_date': (datetime.now() - timedelta(days=5)),
        'max_date': datetime.now()
    }
    return render_template('home.html', **context)

def get_letter_for_units(units):
    """Returns a shorthand letter for the given units."""
    return 'F' if units == 'imperial' else 'C' if units == 'metric' else 'K'

@app.route('/results')
def results():
    """Displays results for current weather conditions."""
    # TODO: Use 'request.args' to retrieve the city & units from the query
    # parameters.
    city = request.args.get('city')
    units = request.args.get('units')
    
    params = {
        # TODO: Enter query parameters here for the 'appid' (your api key),
        "q" : city,
        "appid" : API_KEY,
        "units" : units
        # the city, and the units (metric or imperial).
        # See the documentation here: https://openweathermap.org/current

    }

    result_json = requests.get(API_URL, params=params).json()

    # Uncomment the line below to see the results of the API call!
    #pp.pprint(result_json)

    # TODO: Replace the empty variables below with their appropriate values.
    # You'll need to retrieve these from the result_json object above.
    sunrise_data = result_json["sys"]["sunrise"]
    sunrise_datetime = datetime.fromtimestamp(sunrise_data).strftime('%H:%M')
    sunset_data = result_json["sys"]["sunset"]
    sunset_datetime = datetime.fromtimestamp(sunset_data).strftime('%H:%M')
    # For the sunrise & sunset variables, I would recommend to turn them into
    # datetime objects. You can do so using the `datetime.fromtimestamp()` 
    # function.
    context = {
        'date': datetime.now().strftime('%A, %B %d, %Y'),
        'city': result_json["name"],
        'description': result_json["weather"][0]["description"],
        'temp': result_json["main"]["temp"],
        'humidity': result_json["main"]["humidity"],
        'wind_speed': result_json["wind"]["speed"],
        'sunrise': sunrise_datetime,
        'sunset': sunset_datetime,
        'units_letter': get_letter_for_units(units),
        'icon': result_json["weather"][0]['icon']
    }

    return render_template('results.html', **context)


@app.route('/comparison_results')
def comparison_results():
    """Displays the relative weather for 2 different cities."""
    # TODO: Use 'request.args' to retrieve the cities & units from the query
    # parameters.
    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    units = request.args.get('units')

    # TODO: Make 2 API calls, one for each city. HINT: You may want to write a 
    # helper function for this!
    params = {
        # TODO: Enter query parameters here for the 'appid' (your api key),
        "q" : city1,
        "appid" : API_KEY,
        "units" : units
        # the city, and the units (metric or imperial).
        # See the documentation here: https://openweathermap.org/current

    }
    params2 = {
        # TODO: Enter query parameters here for the 'appid' (your api key),
        "q" : city2,
        "appid" : API_KEY,
        "units" : units
        # the city, and the units (metric or imperial).
        # See the documentation here: https://openweathermap.org/current

    }
    result_json = requests.get(API_URL, params=params).json()
    result_json2 = requests.get(API_URL, params=params2).json()

    # TODO: Pass the information for both cities in the context. Make sure to
    # pass info for the temperature, humidity, wind speed, and sunset time!
    # HINT: It may be useful to create 2 new dictionaries, `city1_info` and 
    # `city2_info`, to organize the data.
    sunrise_data = result_json["sys"]["sunrise"]
    sunrise_datetime = datetime.fromtimestamp(sunrise_data).strftime('%H:%M')
    sunset_data = result_json["sys"]["sunset"]
    sunset_datetime = datetime.fromtimestamp(sunset_data).strftime('%H')

    sunrise_data2 = result_json2["sys"]["sunrise"]
    sunrise_datetime2 = datetime.fromtimestamp(sunrise_data2).strftime('%H:%M')
    sunset_data2 = result_json2["sys"]["sunset"]
    sunset_datetime2 = datetime.fromtimestamp(sunset_data2).strftime('%H')
    temp_comparison = None
    warm_cold = ""
    hum_comparison = None
    hum_gorl = ""
    wind_comparison = None
    wind_gorl = ""
    sunset_comparison = None
    sunset_gorl = ""
    
    #API data pushed into objects
    city1_info = {
        'date': datetime.now().strftime('%A, %B %d, %Y'),
        'city': result_json["name"],
        'description': result_json["weather"][0]["description"],
        'temp': round(result_json["main"]["temp"]),
        'humidity': round(result_json["main"]["humidity"]),
        'wind_speed': round(result_json["wind"]["speed"]),
        'sunrise': sunrise_datetime,
        'sunset': sunset_datetime,
        'units_letter': get_letter_for_units(units),
    }
    city2_info = {
        'city': result_json2["name"],
        'description2': result_json2["weather"][0]["description"],
        'temp2': round(result_json2["main"]["temp"]),
        'humidity2': round(result_json2["main"]["humidity"]),
        'wind_speed2': round(result_json2["wind"]["speed"]),
        'sunrise2': sunrise_datetime2,
        'sunset2': sunset_datetime2,
        'units_letter2': get_letter_for_units(units),
    }
    if city1_info['temp'] > city2_info['temp2']:
        warm_cold = 'warmer'
        temp_comparison = city1_info['temp'] - city2_info['temp2']
    else:
        warm_cold = 'colder'
        temp_comparison = city2_info['temp2'] - city1_info['temp']
    if city1_info['humidity'] > city2_info['humidity2']:
        hum_gorl = 'greater'
        hum_comparison = city1_info['humidity'] - city2_info['humidity2']
    else:
        hum_gorl = 'less'
        hum_comparison = city2_info['humidity2'] - city1_info['humidity'] 
    if city1_info['wind_speed'] > city2_info['wind_speed2']:
        wind_gorl = 'greater'
        wind_comparison = city1_info['wind_speed'] - city2_info['wind_speed2']
    else:
        wind_gorl = 'less'
        wind_comparison = city2_info['wind_speed2'] - city1_info['wind_speed'] 
    if city1_info['sunset'] > city2_info['sunset2']:
        sunset_gorl = 'later'
        sunset_comparison = int(city1_info['sunset']) - int(city2_info['sunset2'])
    else:
        sunset_gorl = 'earlier'
        sunset_comparison = int(city2_info['sunset2']) - int(city1_info['sunset']) 
    

    context = {
        'date': datetime.now().strftime('%A, %B %d, %Y'),
        'city': city1_info["city"],
        'city2': city2_info["city"],
        'units_letter': get_letter_for_units(units),
        'tempcompare': temp_comparison,
        'warmcold': warm_cold,
        'humcompare': hum_comparison,
        'humgorl': hum_gorl,
        'windcompare': wind_comparison,
        'windgorl': wind_gorl,
        'sunsetcompare': sunset_comparison,
        'sunsetgorl': sunset_gorl,
    }

    return render_template('comparison_results.html', **context)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
