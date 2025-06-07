# mini_fb/urls.py
from django.urls import path
from .views import (
    ShowAllProfilesView, ShowProfilePageView, CreateProfileView, 
    CreateStatusMessageView, CreateImageView, UpdateProfileView, 
    DeleteStatusMessageView, UpdateStatusMessageView, AddFriendView,
    ShowFriendSuggestionsView, ShowNewsFeedView
)

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profiles/', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/<int:pk>/create_image', CreateImageView.as_view(), name='create_image'),
    path('profile/<int:pk>/update_profile', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/<int:pk>/delete_status/<int:status_pk>', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('profile/<int:pk>/update_status/<int:status_pk>', UpdateStatusMessageView.as_view(), name='update_status'),
    path('profile/<int:pk>/add_friend/<int:other_pk>', AddFriendView.as_view(), name='add_friend'),
    path('profile/<int:pk>/friend_suggestions', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/<int:pk>/news_feed', ShowNewsFeedView.as_view(), name='news_feed'),
    path('news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),

]