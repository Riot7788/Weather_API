import requests
from django.utils import timezone
from datetime import timedelta
from .models import WeatherQuery
import os

API_KEY = os.getenv("API_KEY")


def get_cached_weather(city, unit):

    five_minutes_ago = timezone.now() - timedelta(minutes=5)


    last_fresh_query = WeatherQuery.objects.filter(
        city__iexact=city,
        timestamp__gte=five_minutes_ago,
        from_cache=False
    ).order_by("-timestamp").first()

    if last_fresh_query:

        temp = convert_temperature(last_fresh_query.temperature, last_fresh_query.unit, unit)

        return WeatherQuery.objects.create(
            city=last_fresh_query.city,
            country=last_fresh_query.country,
            latitude=last_fresh_query.latitude,
            longitude=last_fresh_query.longitude,
            temperature=temp,
            wind_speed=last_fresh_query.wind_speed,
            description=last_fresh_query.description,
            unit=unit,
            from_cache=True
        )
    return None


def get_weather_from_api(city):
    """Погода с внешнего API"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()


def convert_temperature(temp, from_unit, to_unit):
    """Конвертирует температуру между единицами измерения"""
    if temp is None:
        return None

    if from_unit == to_unit:
        return temp

    if from_unit == "C" and to_unit == "F":
        return temp * 9 / 5 + 32
    elif from_unit == "F" and to_unit == "C":
        return (temp - 32) * 5 / 9
    return temp


def save_weather_from_api(weather_data, unit, from_cache=False):
    """Сохраняет данные погоды из API в базу"""
    if weather_data.get("cod") != 200:
        return None

    temp = weather_data["main"]["temp"]
    wind_speed = weather_data["wind"]["speed"]

    if unit == "F":
        temp = convert_temperature(temp, "C", "F")

    temp = round(temp, 1)

    return WeatherQuery.objects.create(
        city=weather_data["name"],
        country=weather_data["sys"]["country"],
        latitude=weather_data["coord"]["lat"],
        longitude=weather_data["coord"]["lon"],
        temperature=temp,
        wind_speed=wind_speed,
        description=weather_data["weather"][0]["description"],
        unit=unit,
        from_cache=from_cache
    )
