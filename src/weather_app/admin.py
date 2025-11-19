from django.contrib import admin

from .models import WeatherQuery


@admin.register(WeatherQuery)
class WeatherQueryAdmin(admin.ModelAdmin):
    list_display = ('city', 'country', 'temperature', 'unit', 'wind_speed', 'timestamp', 'from_cache')
    list_filter = ('from_cache', 'unit', 'timestamp', 'country')
    search_fields = ('city', 'country', 'description')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('city', 'country', 'latitude', 'longitude')
        }),
        ('Погодные данные', {
            'fields': ('temperature', 'unit', 'wind_speed', 'description')
        }),
        ('Метаданные', {
            'fields': ('timestamp', 'from_cache')
        }),
    )
