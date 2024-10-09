import requests
import time

# OpenWeatherAPI
api_key = "1dd5aa3837d3ec1a46e9a72a65841d15"

# function to grab city name's lat and long coordinates
def location(city_name):
    location_request = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={1}&appid={api_key}")
    loc_data = location_request.json()
    if loc_data:
        return loc_data[0]
    else:
        print("City not found.")


# function to pull live weather data from OpenWeatherAPI
def get_weather_data(lat, lon):
    
    data_request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial")

    # checking status of website
    if data_request.status_code == 200:
        data = data_request.json()
        return data
    else:
        print('Error: ', data_request.status_code)
        
        
        
# function to display relevant weather data of chosen location
def display_weather(data):

    # weather info to grab
    city = data['name']
    temperature = data['main']['temp']
    wind_speed = data['wind']['speed']
    weather = data['weather'][0]['main']
    weather_desc = data['weather'][0]['description']
    rain_amount_in_mm = data['rain']['1h']
    rain_in_inches = rain_amount_in_mm / 25.4
    rain_per_hour = round(rain_in_inches, 2)
    
    # weather info to display
    print(f"City: {city}")
    print(f"Temperature: {temperature} F")
    print(f"Weather: {weather}")
    print(f"Rain per hour: {rain_per_hour} inches")
    print(f"Wind Speed: {wind_speed} mph")
    print(f"Description: {weather_desc}")


# user input
city_name = input("Please enter the city you'd like weather data for: ")

# grabbing lat and long coords of city name
location_data = location(city_name)
if location_data:
    lat = location_data['lat']
    lon = location_data['lon']

    
# the script is programmed to update every hour
while True:
    weather_data = get_weather_data(lat, lon)
    display_weather(weather_data)

    print("\nWaiting for the next update...\n")
    time.sleep(3600)   