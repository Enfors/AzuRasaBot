#!/usr/bin/env python3

import configparser
import requests
import sys
import pprint

import datetime


class Weather():

    base_url = "https://api.openweathermap.org/data/2.5/"

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.api_key = api_key = self.config["openweathermap"]["api"]
        self.url_prefix = "https://api.openweathermap.org/data/2.5/"
        self.url_suffix = f"&units=metric&appid={api_key}"

    def get_current_weather(self, location: str):
        url = self.url_prefix + f"weather?q={location}" + self.url_suffix
        result = requests.get(url)
        return result.json()

    def format_weather(self, data, location):
        disp = f"The weather in {location} is as follows:\n"

        disp += f"{data['weather'][0]['description'].capitalize()}, "
        disp += f"{int(data['main']['temp'])} degrees"
        wind = data["wind"]
        wind_speed = int(wind["speed"] + 0.5)

        if wind_speed:
            disp += ", wind at "
            if wind_speed == 1:
                disp += "1 meter "
            else:
                disp += f"{wind_speed} meters "
            disp += "per second "
            disp += f"from the {self.format_direction(wind['deg'])}"

        disp += "."

        return disp

    def format_direction(self, degrees: int):
        cardinals = ["north", "northeast", "east", "southeast",
                     "south", "southwest", "west", "north"]
        return cardinals[int((degrees + 22.5) / 45)]


def get_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["openweathermap"]["api"]


def get_weather(api_key, location):
    url = f"{base_url}weather?q={location}&units=metric&appid={api_key}"
    r = requests.get(url)
    return r.json()


def get_forecast(api_key, location):
    url = f"{base_url}forecast?q={location}&units=metric&appid={api_key}"
    r = requests.get(url)
    return r.json()


def format_direction(degrees):
    cardinals = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    return cardinals[int((degrees + 22.5) / 45)]


def format_item(data, timestamp):
    disp = ""

    disp += datetime.datetime.fromtimestamp(timestamp).\
        strftime("%Y-%m-%d %H:%M: ")
    disp += f"{data['weather'][0]['description'].capitalize()}, "
    disp += f"{int(data['main']['temp'])} C, wind "
    wind = data["wind"]
    disp += f"{format_direction(wind['deg'])} at "
    disp += f"{int(wind['speed'] + 0.5)} m/s."

    return disp

if __name__ == "__main__":
    w = Weather()
    data = w.get_current_weather("Karlstad")
    print(w.format_weather(data))
