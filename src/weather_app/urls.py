from django.urls import path


from .views import (
    home_view,
    query_history,
    export_history_csv,

)

urlpatterns = [
    path("", home_view, name="home"),
    path('query_history/', query_history, name="history"),
    path('export/', export_history_csv, name='export_csv'),

]