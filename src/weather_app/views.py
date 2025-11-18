import requests
import os
from django.http import HttpResponse
from django.shortcuts import render


def home_view(request):

    API_KEY = os.environ.get("API_KEY")

    city = request.GET.get("city","Minsk")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    weather = requests.get(url.format(city)).json()

    if weather.get("cod") == "404":
        return render(request, "home.html", {"error": "Город не найден"})

    city_info = {
        'city': weather["name"],
        'country': weather["sys"]["country"],
        'lat': weather["coord"]["lat"],
        'lon': weather["coord"]["lon"],
        'temp': round(weather["main"]["temp"]),
        'wind_speed': weather["wind"]["speed"],
        'icon': weather["weather"][0]["icon"],
        'description': weather["weather"][0]["description"],
    }

    context = {'info': city_info}

    return render(
        request=request,
        template_name="home.html",
        context=context
    )