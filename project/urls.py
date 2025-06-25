"""
URL configuration for the Project application.
This module defines all the URL patterns for the application, mapping URLs to their
corresponding view functions and classes.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.home, name='home'),
    
    # Generic Views
    path('outfits/', views.OutfitListView.as_view(), name='outfit_list'),
    path('outfits/<int:pk>/', views.OutfitDetailView.as_view(), name='outfit_detail'),
    path('profiles/', views.ProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    
    # Form Views
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    path('create_outfit/', views.CreateOutfitView.as_view(), name='create_outfit'),
    
    # User-specific views
    path('my_profile/', views.MyProfileView.as_view(), name='my_profile'),
    path('friends/', views.FriendsListView.as_view(), name='friends_list'),
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('add_friend/<int:profile_id>/', views.AddFriendView.as_view(), name='add_friend'),
    
    # Authentication - within the project app
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='project/logged_out.html',
        next_page='project:home'
    ), name='logout'),
]