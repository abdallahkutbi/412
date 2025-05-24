from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('restaurant/', views.main, name='main'),
    path('order/', views.order, name='order'), 
    path('confirmation/', views.confirmation, name='confirmation'),
]
