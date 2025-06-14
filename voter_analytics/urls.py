from django.urls import path
from .views import VoterListView
from .views import VoterDetailView
from .views import GraphListView

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter_detail'),
    path('graphs', GraphListView.as_view(), name='graphs'),
]