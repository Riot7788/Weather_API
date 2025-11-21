import csv
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import WeatherQuery

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
            'wind_speed': weather_query.wind_speed,
            'description': weather_query.description,
            'unit': weather_query.unit,
            'icon': icon,
        },
        "from_cache": from_cache,
    }


def query_history(request):

    queries = WeatherQuery.objects.all().order_by('-timestamp')

    paginator = Paginator(queries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(
        request=request,
        template_name="history.html",
        context=context
    )


def export_history_csv(request):
    """Экспорт истории запросов в CSV"""

    queries = WeatherQuery.objects.all().order_by('-timestamp')

    city_filter = request.GET.get('city', '')
    if city_filter:
        queries = queries.filter(city__icontains=city_filter)

    response = HttpResponse(
        content_type='text/csv; charset=utf-8-sig')
    response[
        'Content-Disposition'] = f'attachment; filename="weather_history_{timezone.now().strftime("%Y%m%d_%H%M")}.csv"'

    writer = csv.writer(response, delimiter=';')

    writer.writerow([
        'Город', 'Страна', 'Температура', 'Единицы',
        'Скорость ветра (м/с)', 'Описание', 'Время запроса', 'Из кэша'
    ])

    for query in queries:
        writer.writerow([
            query.city,
            query.country,
            round(query.temperature),
            query.unit,
            f'"{round(query.wind_speed, 1)}"м/с',
            query.description,
            query.timestamp.strftime('%d.%m.%Y %H:%M'),
            'Да' if query.from_cache else 'Нет'
        ])

    return response