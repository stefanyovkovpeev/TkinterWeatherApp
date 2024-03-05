import tkinter as tk
from random import random
import json
import gzip
import random
import requests


class App:

    def __init__(self):
        self.cities = ["New York", "Sofia", "London", "Tokyo", "Sydney"]
        self.weather_data = self.get_weather(self.cities)
        self.city_frames = []
        self.setup_root()
        self.setup_frames()
        self.setup_elements_frame()


    def setup_root(self):
        self.root = tk.Tk()
        self.root.title("Weather Information")
        self.root.geometry("1400x800")

    def setup_frames(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.search_frame = tk.Frame(self.frame)
        self.search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        for city in self.cities:
            self.city_frame = tk.Frame(self.frame, relief=tk.GROOVE, borderwidth=2, width=1400)
            self.city_frame.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
            self.city_frames.append(self.city_frame)

            self.city_label = tk.Label(self.city_frame, text=city, font=("Arial", 16, "bold"))
            self.city_label.pack(pady=5)

        self.summary_frame = tk.Frame(self.frame, relief=tk.GROOVE, borderwidth=2, width=1400)
        self.summary_frame.pack(fill=tk.BOTH, expand=True)


    def setup_elements_frame(self):
        self.search_entry = tk.Entry(self.search_frame, width=30, font=("Arial", 12))
        self.search_entry.pack(side=tk.RIGHT)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_city)
        self.search_button.pack(side=tk.RIGHT, padx=5)

        self.search_result_label = tk.Label(self.search_frame, text="", font=("Arial", 12), fg="red")
        self.search_result_label.pack(side=tk.RIGHT, padx=5)

        self.hottest_label = tk.Label(self.summary_frame, text="", font=("Arial", 14))
        self.hottest_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.coldest_label = tk.Label(self.summary_frame, text="", font=("Arial", 14))
        self.coldest_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.average_label = tk.Label(self.summary_frame, text="", font=("Arial", 14))
        self.average_label.pack(side=tk.LEFT, padx=10, pady=5)
        weather_data = self.get_weather(self.cities)
        self.temperature_labels = []
        self.humidity_labels = []
        self.conditions_labels = []
        for i, city in enumerate(self.cities):
            self.temperature_label = tk.Label(self.city_frames[i],
                                              text=f"Temperature: {weather_data[city]['temp_current']}°C",
                                              font=("Arial", 14))
            self.temperature_label.pack(side=tk.LEFT, padx=10)
            self.temperature_labels.append(self.temperature_label)

            self.humidity_label = tk.Label(self.city_frames[i], text=f"Humidity: {weather_data[city]['humidity']}",
                                           font=("Arial", 14))
            self.humidity_label.pack(side=tk.LEFT, padx=10)
            self.humidity_labels.append(self.humidity_label)

            self.conditions_label = tk.Label(self.city_frames[i],
                                             text=f"Conditions: {weather_data[city]['conditions']}",
                                             font=("Arial", 14))
            self.conditions_label.pack(side=tk.LEFT, padx=10)
            self.conditions_labels.append(self.conditions_label)

        self.update_button = tk.Button(self.search_frame, text="Update Weather", command=self.update_weather, font=("Arial", 14))
        self.update_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.generate_button = tk.Button(self.search_frame, text="Generate Random Cities",
                                         command=self.random_cities_generator, font=("Arial", 14))
        self.generate_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="center")

        self.avarages_elements_setup()

    def avarages_elements_setup(self):
        weather_data = self.get_weather(self.cities)
        self.temperatures = [weather_data[city]['temp_current'] for city in self.cities]
        self.hottest_city = self.cities[self.temperatures.index(max(self.temperatures))]
        self.average_temperature = sum(self.temperatures) / len(self.temperatures)

        self.hottest_label.config(text=f"Hottest City: {self.hottest_city} ({max(self.temperatures)}°C)")
        self.average_label.config(text=f"Average Temperature From All: {self.average_temperature :.2f}°C")

    def random_cities_generator(self):
        url = "http://bulk.openweathermap.org/sample/city.list.json.gz"

        response = requests.get(url)

        if response.status_code == 200:
            with open("city_data.json.gz", "wb") as f:
                f.write(response.content)

            with gzip.open("city_data.json.gz", "rb") as f:
                city_data = json.load(f)

            city_names = [city['name'] for city in city_data]

            random_cities = random.sample(city_names, 5)

        else:
            self.search_result_label.config(text=f"Unable to fetch data now.")

        self.cities = random_cities

    def get_weather(self, cities):
        self.weather_data = {}

        base_url = "http://api.openweathermap.org/data/2.5/weather"
        for city in cities:
            params = {
                'q': city,
                'appid': "***",
                'units': 'metric'
            }
            response = requests.get(base_url, params=params)
            data = response.json()

            conditions = data['weather'][0]['description']
            temp_current = round(data['main']['temp'])
            humidity = data['main']['humidity']

            self.weather_data[city] = {
                'conditions': conditions,
                'temp_current': temp_current,
                'humidity': humidity
            }

        return self.weather_data

    def search_city(self):
        try:
            city = self.search_entry.get().casefold()

            base_url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': "***",
                'units': 'metric'
            }
            response = requests.get(base_url, params=params)
            data = response.json()

            conditions = data['weather'][0]['description']
            temp_current = round(data['main']['temp'])
            humidity = data['main']['humidity']

            city_window = tk.Toplevel(self.root)
            city_window.title(city)

            temperature_label = tk.Label(city_window, text=f"Temperature: {temp_current}°C",
                                         font=("Arial", 14))
            temperature_label.pack(padx=10, pady=5)

            humidity_label = tk.Label(city_window, text=f"Humidity: {humidity}", font=("Arial", 14))
            humidity_label.pack(padx=10, pady=5)

            conditions_label = tk.Label(city_window, text=f"Conditions: {conditions}",
                                        font=("Arial", 14))
            conditions_label.pack(padx=10, pady=5)

        except:
            self.search_result_label.config(text=f"City '{city}' not found")


    def update_weather(self):
            weather_data = self.get_weather(self.cities)
            for i, city in enumerate(self.cities):
                city_label = self.city_frames[i].winfo_children()[0]
                city_label.config(text=city)

            for i, city in enumerate(self.cities):
                self.temperature_labels[i].config(text=f"Temperature: {weather_data[city]['temp_current']}°C")
                self.humidity_labels[i].config(text=f"Humidity: {weather_data[city]['humidity']}")
                self.conditions_labels[i].config(text=f"Conditions: {weather_data[city]['conditions']}")

            self.avarages_elements_setup()






if __name__ == "__main__":
    app = App()
    app.root.mainloop()