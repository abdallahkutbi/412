"""
urls.py
Defines URL patterns for the Project app, mapping URLs to their corresponding views.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import EditOutfitView, FeedView, DeleteOutfitView, DebugLoginView
from django.contrib.auth.views import LoginView

app_name = 'project'

urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    
    path('outfits/', views.OutfitListView.as_view(), name='outfit_list'),
    path('outfits/<int:pk>/', views.OutfitDetailView.as_view(), name='outfit_detail'),
    path('profiles/', views.ProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    path('create_outfit/', views.CreateOutfitView.as_view(), name='create_outfit'),
    path('add_item/', views.add_item, name='add_item'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    
    path('my_profile/', views.MyProfileView.as_view(), name='my_profile'),
    path('friends/', views.FriendsListView.as_view(), name='friends_list'),
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('add_friend/<int:profile_id>/', views.AddFriendView.as_view(), name='add_friend'),
    path('remove_friend/<int:pk>/', views.remove_friend, name='remove_friend'),
    
    path('login/', LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='project/logged_out.html',
        next_page='project:feed',
        http_method_names=['get', 'post']
    ), name='logout'),
    
    path('edit_outfit/<int:pk>/', EditOutfitView.as_view(), name='edit_outfit'),
    path('delete_outfit/<int:pk>/', DeleteOutfitView.as_view(), name='delete_outfit'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
]