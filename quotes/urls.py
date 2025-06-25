from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path('', home, name='quotes'),
    path('quotes/', home, name='quotes'),
    path('show_all/', show_all, name='show_all'),
    path('about/', about, name='about'),
]
