import requests
import time

# OpenWeatherAPI
api_key = "1dd5aa3837d3ec1a46e9a72a65841d15"

# user input
msg1 = print("Please enter the latitude and longtitude of the location you want the weather information of: (Use three decimals)\n")
lat = input("Latitude: ")
lon = input("Longitude: ")
print("")
time.sleep(1)




# function to pull live weather data from OpenWeatherAPI
def get_weather_data(lat, lon):
    
    data_request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial")

    # checking status of website
    if data_request.status_code == 200:
        data = data_request.json()
        return data
    else:
        print('Error: ', data_request.status_code)
        return None
        
        
# function to display relevant weather data of chosen location
def display_weather(data):

    city = data['name']
    temperature = data['main']['temp']
    wind_speed = data['wind']['speed']
    weather_desc = data['weather'][0]['description']

    print(f"City: {city}")
    print(f"Temperature: {temperature} F")
    print(f"Weather: {wind_speed} mph")
    print(f"Description: {weather_desc}")


weather_data = get_weather_data(lat, lon)
display_weather(weather_data)

    





































