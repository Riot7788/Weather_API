from django.urls import path


from .views import (
    home_view,
    query_history,

)

urlpatterns = [
    path("", home_view, name="home"),
    path('query_history/', query_history, name="history"),

]