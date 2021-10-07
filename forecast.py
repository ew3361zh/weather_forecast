"""
Weather Forecast 
"""
import os
import requests
from datetime import datetime
from pprint import pprint
import logging

# Configure the logger - what file to write log messages to,
# and what log level messages (and higher) should be written
logging.basicConfig(filename='forecast.log', level=logging.INFO)

def main():

    city = input(f'For what city would you like to get a forecast? ')
    country = input(f'And what is the 2-letter country-code where {city} is located? ')
    
    try:
        list_of_forecasts = get_forecast(city, country)
        forecast_data = list_of_forecasts['list']

        if forecast_data:
            forecast_output(forecast_data, city, country)

        else:
            print('This location was not found.')
            logging.info('Location %s, %s not found' % (city, country))

    except Exception as e:
        logging.exception('Error fetching current weather data for %s, %s' % (city, country)) 
        print('Sorry, there was an error fetching data. '
              'Please check your internet connection, and if that\'s ok, report this to the developer.', e)


def get_forecast(city, country):

    """
    Query the Open Weather Map API for the current conditions for a city and country.
    Returns the JSON from Open Weather Map if the location is found
    Return None if the location is not found
    Raises an exception if connection error, API key error etc.
    """

    url = 'http://api.openweathermap.org/data/2.5/forecast'

    key = os.environ.get('WEATHER_KEY')
    assert key is not None # raises an error if environment variable is not set
    if key is None: 
        logging.info('Key logged as None')

    query_locale = f'{city},{country}'
    query = {'q':query_locale,'units':'imperial','appid':key}

    data_response = requests.get(url, params=query)

    # Status codes of 200 mean the request was received and processed without error
    if data_response.status_code == 200:
        return data_response.json()
    # The API returns 404 (Not Found) if the location can't be found. Check for this and return None
    if data_response.status_code == 404:
        return None

    # Any other errors, raise an exception
    data_response.raise_for_status()  # Raise an exception if the status code is not 2xx or 3xx


def forecast_output(list_of_forecasts, city, country):

    """
    pulling data out of forecast API Json response and printing it in a more readable way for the user.

    """
    
    print(f'Your five day forecast for {city.capitalize()}, {country.upper()}')
    for forecast in list_of_forecasts:
        weather = forecast['weather'][0]['description']
        windspeed = forecast['wind']['speed']
        temp = forecast['main']['temp']
        timestamp = forecast['dt']
        # making time local to location for user sake because program should output data in a frame of reference they will most likely understand
        forecast_date = datetime.fromtimestamp(timestamp)
        humidity = forecast['main']['humidity']
        print(f'On {forecast_date}: \n {weather} with a temp of {temp}F and {humidity}% humidity and a wind of {windspeed}mph')
        # logging selected weather result to show successful query
        logging.info('Successful query with result: weather is ' + weather)

if __name__ == '__main__':
    main()