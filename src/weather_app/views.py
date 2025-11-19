import requests
import os
from django.http import HttpResponse
from django.shortcuts import render

from .service import (
    get_cached_weather,
    get_weather_from_api,
    save_weather_from_api,
)


def home_view(request):

    city = request.GET.get("city", "Minsk")
    unit = request.GET.get("unit", "C")

    cached_query = get_cached_weather(city, unit)
    if cached_query:
        context = create_context_from_query(cached_query, from_cache=True)
        return render(request, "home.html", context)

    weather_data = get_weather_from_api(city)

    if weather_data.get("cod") != 200:
        return render(request, "home.html", {
            "error": f"Город '{city}' не найден",
            "city": city
        })

    weather_query = save_weather_from_api(weather_data, unit, from_cache=False)
    context = create_context_from_query(weather_query, from_cache=False, weather_data=weather_data)

    return render(request, "home.html", context)


def create_context_from_query(weather_query, from_cache=False, weather_data=None):
    """Создаёт контекст для шаблона из объекта WeatherQuery"""

    icon = ""
    if weather_data and not from_cache:
        icon = weather_data["weather"][0]["icon"]

    return {
        "info": {
            'city': weather_query.city,
            'country': weather_query.country,
            'lat': weather_query.latitude,
            'lon': weather_query.longitude,
            'temp': round(weather_query.temperature),
            'wind_speed': weather_query.wind_speed,  # Всегда в м/с
            'description': weather_query.description,
            'unit': weather_query.unit,
            'icon': icon,
        },
        "from_cache": from_cache,
    }
