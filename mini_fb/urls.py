"""
URL configuration for the Mini Facebook application.
This module defines all the URL patterns for the application, mapping URLs to their
corresponding view functions and classes.
"""

# mini_fb/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    ShowAllProfilesView, ShowProfilePageView, CreateProfileView, 
    CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, 
    UpdateStatusMessageView, AddFriendView, ShowFriendSuggestionsView, 
    ShowNewsFeedView, ShowMyProfileView, LogoutConfirmationView
)

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),

    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/news_feed/<int:pk>/', ShowNewsFeedView.as_view(), name='news_feed'),
    path('profile/<int:pk>/add_friend/<int:other_pk>/', AddFriendView.as_view(), name='add_friend'),
    path('profile/friend_suggestions/<int:pk>/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('status/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/my/', ShowMyProfileView.as_view(), name='my_profile'),
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='mini_fb/logged_out.html',
        next_page='show_all_profiles'
    ), name='logout'),
    path('logout_confirmation/', LogoutConfirmationView.as_view(), name='logout_confirmation'),

]