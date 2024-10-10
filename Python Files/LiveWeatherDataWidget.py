from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QLabel, QWidget, QVBoxLayout
from WeatherDataOfFlorida import *
import sys
import requests
import time

# OpenWeatherAPI
api_key = "1dd5aa3837d3ec1a46e9a72a65841d15"

# function to grab city name's lat and long coordinates
def location(city_name):
    location_request = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={3}&appid={api_key}")
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

    #### currently not working ####
    # rain_amount_in_mm = data['rain'][0]['1h']
    # rain_in_inches = rain_amount_in_mm / 25.4
    # rain_per_hour = round(rain_in_inches, 2)
    
    
    # weather info to display
    return (f"City: {city}\n"
        f"Temperature: {temperature} F\n"
        f"Weather: {weather}\n"
        #f"Rain per hour: {rain_per_hour} inches"
        f"Wind Speed: {wind_speed} mph\n"
        f"Description: {weather_desc}\n")






class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # GUI window title
        self.setWindowTitle("Live Florida Weather")
        self.setGeometry(100,100,600,400)

        # Create main layout and widget
        self.layout = QVBoxLayout()
        self.container = QWidget()

        # Create input field for city name
        self.city_input = QLineEdit()
        self.city_input.setMaxLength(50)
        self.city_input.setPlaceholderText("Enter city name...")
        self.city_input.returnPressed.connect(self.return_pressed)

        # Create button to fetch weather
        self.button = QPushButton("Get Weather")
        self.button.clicked.connect(self.buttonMethod)

        # Create label to display results
        self.result_label = QLabel()

        # Add widgets to layout
        self.layout.addWidget(self.city_input)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.result_label)

        # Set the layout to the main window
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        # GUI styling CSS
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                font-size: 14px;
                padding: 10px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
        """)

    
    def buttonMethod(self):
        # Get the city name from QLineEdit
        city_name = self.city_input.text()

        if city_name:
            # Fetch latitude and longitude for the city
            location_data = location(city_name)

            if location_data:
                lat = location_data['lat']
                lon = location_data['lon']

                # Fetch weather data
                weather_data = get_weather_data(lat, lon)
                
                # Display weather data in QLabel
                weather_info = display_weather(weather_data)
                self.result_label.setText(weather_info)
            else:
                self.result_label.setText("City not found. Please enter a valid city name.")
        else:
            self.result_label.setText("Please enter a city name.")

            

    # does the same thing as buttonMethod if Return key is pressed
    def return_pressed(self):
        city_name = self.city_input.text()

        if city_name:
            # Fetch latitude and longitude for the city
            location_data = location(city_name)

            if location_data:
                lat = location_data['lat']
                lon = location_data['lon']

                # Fetch weather data
                weather_data = get_weather_data(lat, lon)
                
                # Display weather data in QLabel
                weather_info = display_weather(weather_data)
                self.result_label.setText(weather_info)
            else:
                self.result_label.setText("City not found. Please enter a valid city name.")
        else:
            self.result_label.setText("Please enter a city name.")
        
# Create the application
app = QApplication(sys.argv)

# Create and show the main window
window = MainWindow()
window.show()

# Run the event loop
app.exec()



