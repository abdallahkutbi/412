"""
Views for the Mini Facebook application.
This module contains all the view classes that handle different pages and actions
in the Mini Facebook application, including profile views, status message views,
and friend management views.
"""

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, StatusMessage, Image, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm, CreateImageForm, UpdateProfileForm
from django.urls import reverse
# Create your views here.
class ShowAllProfilesView(ListView):
    '''
    View to show all profiles
    '''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'


class ShowProfilePageView(DetailView):
    '''
    Display a single profile
    '''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'


class CreateProfileView(CreateView):
    '''
    View to create a new profile
    '''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    context_object_name = 'profile'


class CreateStatusMessageView(CreateView):
    '''
    View to create a new status message
    '''
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context      
    
    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(pk=self.kwargs['pk'])
        sm = form.save()
        
        files = self.request.FILES.getlist('files')
        for f in files:
            image = Image.objects.create(
                image_file=f,
                profile=form.instance.profile
            )
            StatusImage.objects.create(
                status_message=sm,
                image=image
            )
        
        return super().form_valid(form)
    

class CreateImageView(CreateView):
    '''
    View to create a new image
    '''
    model = Image
    form_class = CreateImageForm
    template_name = 'mini_fb/create_image_form.html'
    context_object_name = 'image'

class UpdateProfileView(UpdateView):
    '''
    View to update a profile
    '''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    context_object_name = 'profile'

class DeleteStatusMessageView(DeleteView):
    '''
    View to delete a status message
    '''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_object(self):
        return StatusMessage.objects.get(pk=self.kwargs['status_pk'])

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

class UpdateStatusMessageView(UpdateView):
    '''
    View to update a status message
    '''
    model = StatusMessage
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'
    fields = ['message']

    def get_object(self):
        return StatusMessage.objects.get(pk=self.kwargs['status_pk'])

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

class AddFriendView(View):
    '''
    View to add a friend relationship
    '''
    def dispatch(self, request, *args, **kwargs):
        # Get the profiles from the URL parameters
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        other_profile = Profile.objects.get(pk=self.kwargs['other_pk'])
        
        # Add the friend relationship
        profile.add_friend(other_profile)
        
        # Redirect back to the profile page
        return redirect('show_profile', pk=profile.pk)

class ShowFriendSuggestionsView(DetailView):
    '''
    View to show friend suggestions
    '''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suggestions'] = self.object.get_friend_suggestions()
        return context

class ShowNewsFeedView(DetailView):
    '''
    View to show status messages from friends and self in the news feed
    '''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_messages'] = self.object.get_news_feed()
        return context
    
