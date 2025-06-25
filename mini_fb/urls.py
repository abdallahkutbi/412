"""
URL configuration for mini_fb app.
"""

from django.urls import path
from . import views

app_name = 'mini_fb'

urlpatterns = [
    path('', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    path('create_status/<int:pk>/', views.CreateStatusMessageView.as_view(), name='create_status'),
    path('update_profile/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('delete_status/<int:pk>/', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path('update_status/<int:pk>/', views.UpdateStatusMessageView.as_view(), name='update_status'),
    path('add_friend/<int:pk>/<int:other_pk>/', views.AddFriendView.as_view(), name='add_friend'),
    path('friend_suggestions/<int:pk>/', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('news_feed/<int:pk>/', views.ShowNewsFeedView.as_view(), name='news_feed'),
    path('my_profile/', views.ShowMyProfileView.as_view(), name='my_profile'),
    path('logout/', views.LogoutConfirmationView.as_view(), name='logout'),
]