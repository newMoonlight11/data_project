from django.urls import path
from data_app.views import parse_file, home

urlpatterns = [
    path('', home), 
    path('parse/', parse_file, name='parse_file'),
]