"""
Views for the Project application.
This module defines all the views for the application, including views for creating and updating profiles and outfits.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Outfit, Friend, ProfileImage, OutfitImage, OutfitItem
from .forms import CreateProfileForm, CreateOutfitForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def home(request):
    """Home page showing recent outfits"""
    try:
        recent_outfits = Outfit.objects.all().order_by('-timestamp')[:6]
    except:
        # Fallback if timestamp field doesn't exist yet
        recent_outfits = Outfit.objects.all()[:6]
    
    context = {
        'recent_outfits': recent_outfits,
    }
    return render(request, 'project/home.html', context)

# Generic Views
class OutfitListView(ListView):
    model = Outfit
    template_name = 'project/outfit_list.html'
    context_object_name = 'outfits'
    
    def get_queryset(self):
        try:
            return Outfit.objects.all().order_by('-timestamp')
        except:
            # Fallback if timestamp field doesn't exist yet
            return Outfit.objects.all()

class OutfitDetailView(DetailView):
    model = Outfit
    template_name = 'project/outfit_detail.html'
    context_object_name = 'outfit'

class ProfileListView(ListView):
    model = Profile
    template_name = 'project/profile_list.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'project/profile_detail.html'
    context_object_name = 'profile'

# Login Required Views
class CreateOutfitView(LoginRequiredMixin, CreateView):
    """Create a new outfit"""
    model = Outfit
    form_class = CreateOutfitForm
    template_name = 'project/create_outfit.html'
    context_object_name = 'outfit'

    def form_valid(self, form):
        form.instance.profile = self.request.user.project_profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project:home')

    def get_login_url(self):
        return reverse('project:login')

class CreateProfileView(CreateView):
    """Create a new profile with user account"""
    model = Profile
    form_class = CreateProfileForm
    template_name = 'project/create_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = UserCreationForm(self.request.POST)
        else:
            context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user)
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

    def get_success_url(self):
        return reverse('project:home')

class MyProfileView(LoginRequiredMixin, DetailView):
    """Show current user's profile"""
    model = Profile
    template_name = 'project/my_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        try:
            return self.request.user.project_profile
        except Profile.DoesNotExist:
            return None

    def get_login_url(self):
        return reverse('project:login')

class FriendsListView(LoginRequiredMixin, DetailView):
    """Show current user's friends"""
    model = Profile
    template_name = 'project/friends_list.html'
    context_object_name = 'profile'

    def get_object(self):
        try:
            return self.request.user.project_profile
        except Profile.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['friends'] = self.object.get_friends()
        return context

    def get_login_url(self):
        return reverse('project:login')

class FeedView(LoginRequiredMixin, DetailView):
    """Show feed with friends' outfits"""
    model = Profile
    template_name = 'project/feed.html'
    context_object_name = 'profile'

    def get_object(self):
        try:
            return self.request.user.project_profile
        except Profile.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['outfits'] = self.object.get_news_feed()
        return context

    def get_login_url(self):
        return reverse('project:login')

class AddFriendView(LoginRequiredMixin, View):
    """Add a friend"""
    def dispatch(self, request, *args, **kwargs):
        try:
            profile = request.user.project_profile
            friend_profile = get_object_or_404(Profile, pk=self.kwargs['profile_id'])
            
            if profile.add_friend(friend_profile):
                messages.success(request, f'Added {friend_profile.first_name} as a friend!')
            else:
                messages.warning(request, 'Already friends or cannot add yourself!')
                
        except Profile.DoesNotExist:
            return redirect('project:create_profile')
        
        return redirect('project:profile_detail', pk=self.kwargs['profile_id'])

    def get_login_url(self):
        return reverse('project:login')

def outfit_list(request):
    outfits = Outfit.objects.all().order_by('-created_at')
    return render(request, 'project/outfit_list.html', {'outfits': outfits})

def outfit_detail(request, pk):
    outfit = get_object_or_404(Outfit, pk=pk)
    return render(request, 'project/outfit_detail.html', {'outfit': outfit})

def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'project/profile_list.html', {'profiles': profiles})

def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'project/profile_detail.html', {'profile': profile})

@login_required
def my_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    # handle edit logic here
    return render(request, 'project/my_profile.html', {'profile': profile})

@login_required
def friends_list(request):
    profile = get_object_or_404(Profile, user=request.user)
    friends = profile.friends.all()
    return render(request, 'project/friends_list.html', {'friends': friends})

@login_required
def news_feed(request):
    profile = get_object_or_404(Profile, user=request.user)
    friends = profile.friends.all()
    outfits = Outfit.objects.filter(user__in=friends).order_by('-created_at')
    return render(request, 'project/news_feed.html', {'outfits': outfits})