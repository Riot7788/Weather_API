# Weather API Application
Веб-приложение для получения текущей погоды с кэшированием, историей запросов и экспортом данных.

## Основные функции
- **Поиск погоды** - получение текущих данных о погоде по названию города
- **Кэширование** - повторные запросы одного города в течение 5 минут возвращаются из кэша
- **История запросов** - просмотр всех предыдущих запросов с фильтрацией и пагинацией
- **Экспорт в CSV** - выгрузка истории запросов в CSV формате
- **Мультиязычные единицы** - поддержка °C и °F
- **Админ-панель** - управление данными через Django Admin

## Технологический стек
- **Backend**: Django 5.2, Python 3.11
- **Database**: PostgreSQL
- **Frontend**: HTML, Bootstrap, Django Templates
- **API**: OpenWeatherMap
- **Containerization**: Docker, Docker Compose
- **Cache**: Database-based caching

### Предварительные требования
- Docker Desktop
- API ключ OpenWeatherMap

### 1. Клонирование и настройка
```bash
git clone https://github.com/Riot7788/Weather_API.git
cd Weather_API/src