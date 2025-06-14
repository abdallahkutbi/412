"""
Views for the Mini Facebook application.
This module contains all the view classes that handle different pages and actions
in the Mini Facebook application, including profile views, status message views,
and friend management views.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, StatusMessage, Image
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateProfileForm, CreateStatusMessageForm, CreateImageForm, UpdateProfileForm
from django.urls import reverse
from django.views.generic import TemplateView

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['friends'] = profile.get_friends()
        context['suggested_friends_preview'] = profile.get_friend_suggestions()[:4]
        return context


class CreateProfileView(CreateView):
    '''
    View to create a new profile
    '''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    context_object_name = 'profile'

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''
    View to create a new status message
    '''
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    context_object_name = 'status_message'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        profile= Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile

        sm = form.save()
        files = self.request.FILES.getlist('files')
        for file in files: 
            image = Image.objects.create(status=sm, image_file=file)
            image.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    
    def get_login_url(self):
        return reverse('login')

class CreateImageView(CreateView):
    '''
    View to create a new image
    '''
    model = Image
    form_class = CreateImageForm
    template_name = 'mini_fb/create_image_form.html'
    context_object_name = 'image'

class UpdateProfileView(LoginRequiredMixin, UpdateView): 
    '''
    View to update a profile
    '''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self):
        for p in Profile.objects.all():
            if p.user.pk == self.request.user.pk: 
                return p
        return

    def get_login_url(self):
        return reverse('login')

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''
    View to delete a status message
    '''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_object(self):
        return StatusMessage.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        status = self.get_object()
        return reverse('show_profile', kwargs={'pk': status.profile.pk})

    def get_login_url(self):
        return reverse('login')

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''
    View to update a status message
    '''
    model = StatusMessage
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'
    fields = ['message']

    def get_object(self):
        return StatusMessage.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        status = self.get_object()
        return reverse('show_profile', kwargs={'pk': status.profile.pk})

    def get_login_url(self):
        return reverse('login')

class AddFriendView(LoginRequiredMixin, View):
    '''
    View to add a friend relationship
    '''
    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        other_profile = Profile.objects.get(pk=self.kwargs['other_pk'])
        
        profile.add_friend(other_profile)
        
        return redirect('show_profile', pk=profile.pk)

    def get_login_url(self):
        return reverse('login')

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
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

    def get_login_url(self):
        return reverse('login')

class ShowNewsFeedView(LoginRequiredMixin, DetailView ):
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

    def get_login_url(self):
        return reverse('login')


class LogoutConfirmationView(TemplateView):
    '''
    Render the logout confirmation page.
    '''
    template_name = "mini_fb/logged_out.html"


class ShowMyProfileView(LoginRequiredMixin, DetailView):
    '''
    View of my Profile
    '''
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context["friends"] = profile.get_friends()
        context["suggested_friends_preview"] = profile.get_friend_suggestions()[:4]
        return context

    def get_login_url(self):
        return reverse('login')

    
def create_profile(request):
    """
    Handles the creation of a new Profile.
    """
    if request.method == "POST":
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_all_profiles')
    else:
            form = CreateProfileForm()
    return render(request, "mini_fb/create_profile.html", {"form": form})