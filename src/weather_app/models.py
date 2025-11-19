from django.db import models
from django.utils import timezone


class WeatherQuery(models.Model):
    UNIT_CHOICES = [
        ("C", "Celsius"),
        ("F", "Fahrenheit"),
    ]

    city = models.CharField(max_length=100, verbose_name='Город')
    country = models.CharField(max_length=20, blank=True, verbose_name='Страна')
    latitude = models.FloatField(null=True, blank=True, verbose_name='Широта')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Долгота')
    temperature = models.FloatField(verbose_name='Температура')
    wind_speed = models.FloatField(null=True, blank=True, verbose_name='Скорость ветра')
    description = models.CharField(max_length=255, verbose_name='Описание погоды')

    unit = models.CharField(
        max_length=1,
        choices=UNIT_CHOICES,
        default="C",
        verbose_name='Единицы измерения'
    )
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='Время запроса')
    from_cache = models.BooleanField(default=False, verbose_name='Из кэша')

    class Meta:
        verbose_name = 'Запрос погоды'
        verbose_name_plural = 'Запросы погоды'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        cache_status = " (кэш)" if self.from_cache else ""
        return f"{self.city} - {self.temperature}°{self.unit} - {self.timestamp.strftime('%d.%m.%Y %H:%M')}{cache_status}"
