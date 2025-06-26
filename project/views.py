from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse, reverse_lazy
from .models import Profile, Outfit, Friend, OutfitItem
from .forms import CreateProfileForm, OutfitForm, OutfitItemForm, CreateOutfitItemForm
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from django.db import models
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import LoginView

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'project/profile_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        # Exclude the current user's profile if it exists
        return Profile.objects.exclude(username=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get the current user's profile
        try:
            user_profile = Profile.objects.get(username=user)
            # Use the get_friends() method to get the list of friends
            context['friends'] = user_profile.get_friends()
        except Profile.DoesNotExist:
            # If user doesn't have a profile yet, return empty list
            context['friends'] = []
        
        return context

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'project/profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['friends'] = profile.get_friends()
        context['suggested_friends_preview'] = profile.get_friend_suggestions()[:4]
        context['outfits'] = profile.get_outfits()
        return context

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'project/create_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        print("DEBUG: Entered form_valid in CreateProfileView")
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            print("DEBUG: UserCreationForm is valid")
            user = user_form.save()
            print(f"DEBUG: Created user: {user} (id={user.id})")
            login(self.request, user)
            print(f"DEBUG: After login, request.user: {self.request.user}, is_authenticated: {self.request.user.is_authenticated}")
            
            # The signal should have already created a profile, so just get it
            try:
                profile = Profile.objects.get(username=user)
                print(f"DEBUG: Found existing profile for user {user.username} (id={user.id})")
            except Profile.DoesNotExist:
                # Fallback: create profile if signal didn't work
                profile = Profile.objects.create(username=user)
                print(f"DEBUG: Created new profile for user {user.username} (id={user.id})")
            
            # Update the profile fields with form data
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.city = form.cleaned_data['city']
            profile.email = form.cleaned_data['email']
            profile.bio = form.cleaned_data.get('bio', '')
            profile.profile_image = form.cleaned_data.get('profile_image', None)
            profile.save()
            print(f"DEBUG: Profile updated for user {user.username} (id={user.id})")
            return redirect(self.get_success_url())
        else:
            print("DEBUG: UserCreationForm is NOT valid")
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

    def get_success_url(self):
        return reverse('project:my_profile')

class MyProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'project/my_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        #return get_object_or_404(Profile, username=self.request.user)
        return Profile.objects.filter(username=self.request.user).last()

class OutfitListView(ListView):
    model = Outfit
    template_name = 'project/outfit_list.html'
    context_object_name = 'outfits'

    def get_queryset(self):
        return Outfit.objects.all().order_by('-timestamp')

class OutfitDetailView(DetailView):
    model = Outfit
    template_name = 'project/outfit_detail.html'
    context_object_name = 'outfit'

class CreateOutfitView(LoginRequiredMixin, CreateView):
    model = Outfit
    fields = ['subject', 'items']
    template_name = 'project/create_outfit.html'
    context_object_name = 'outfit'

    def form_valid(self, form):
        profile = Profile.objects.filter(username=self.request.user).last()
        if not profile:
            # Optionally, redirect to create profile if none exists
            return redirect('project:create_profile')
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project:my_profile')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filter from query params
        item_type = self.request.GET.get('item_type', '')
        
        # Filter items by type if specified
        items = OutfitItem.objects.filter(owner=self.request.user)
        if item_type:
            items = items.filter(item_type=item_type)
        
        # Add all the context variables the template expects
        context['items'] = items
        context['item_types'] = OutfitItem.ITEM_TYPES
        context['selected_type'] = item_type
        
        return context

class FriendsListView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'project/friends_list.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(Profile, username=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends'] = self.object.get_friends()
        return context

class FeedView(DetailView):
    model = Profile
    template_name = 'project/feed.html'
    context_object_name = 'profile'

    def get_object(self):
        if self.request.user.is_authenticated:
            return Profile.objects.filter(username=self.request.user).last()
        return None  # or handle anonymous users as needed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['outfits'] = self.object.get_news_feed()
            context['friends'] = self.object.get_friends()
        else:
            # Show all outfits or a public feed for anonymous users
            from .models import Outfit
            context['outfits'] = Outfit.objects.all().order_by('-timestamp')
            context['friends'] = []
        return context

class AddFriendView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        profile = Profile.objects.filter(username=request.user).last()
        friend_profile = get_object_or_404(Profile, pk=self.kwargs['profile_id'])
        profile.add_friend(friend_profile)
        return redirect('project:profile_list')

class HomeView(TemplateView):
    template_name = 'project/home.html'

@login_required
def create_outfit(request):
    item_type = request.GET.get('item_type', '')  # Get filter from query params
    items = OutfitItem.objects.filter(owner=request.user)
    if item_type:
        items = items.filter(item_type=item_type)
    if request.method == 'POST':
        form = OutfitForm(request.POST)
        selected_items = request.POST.getlist('items')
        if form.is_valid():
            profile = Profile.objects.filter(username=request.user).last()
            outfit = form.save(commit=False)
            outfit.profile = profile
            outfit.save()
            for item_id in selected_items:
                item = OutfitItem.objects.get(id=item_id)
                outfit.items.add(item)
            return redirect('project:outfit_detail', pk=outfit.pk)
    else:
        form = OutfitForm()
    # Pass all item types for the dropdown
    item_types = OutfitItem.ITEM_TYPES
    return render(request, 'project/create_outfit.html', {
        'form': form,
        'items': items,
        'item_types': item_types,
        'selected_type': item_type,
    })

def add_outfit_item(request):
    if request.method == 'POST':
        form = OutfitItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user  # Add an owner field to OutfitItem if needed
            item.save()
            return redirect('add_outfit_item')
    else:
        form = OutfitItemForm()
    # Show only items not assigned to an outfit
    items = OutfitItem.objects.filter(owner=request.user, outfit=None)
    return render(request, 'project/add_outfit_item.html', {'form': form, 'items': items})

@login_required
def add_item(request):
    if request.method == 'POST':
        form = OutfitItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            return redirect('project:add_item')
    else:
        form = OutfitItemForm()
    items = OutfitItem.objects.filter(owner=request.user)
    return render(request, 'project/add_item.html', {'form': form, 'items': items})

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(OutfitItem, id=item_id, owner=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('project:add_item')
    return render(request, 'project/confirm_delete_item.html', {'item': item})

@login_required
def edit_item(request, item_id):
    item = get_object_or_404(OutfitItem, id=item_id, owner=request.user)
    if request.method == 'POST':
        form = OutfitItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('project:add_item')
    else:
        form = OutfitItemForm(instance=item)
    return render(request, 'project/edit_item.html', {'form': form, 'item': item})

@method_decorator(login_required, name='dispatch')
class EditOutfitView(LoginRequiredMixin, UpdateView):
    model = Outfit
    form_class = OutfitForm
    template_name = 'project/edit_outfit.html'
    context_object_name = 'outfit'

    def get_queryset(self):
        # Only allow editing outfits owned by the current user
        return Outfit.objects.filter(profile__username=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the user's items for selection
        context['items'] = OutfitItem.objects.filter(owner=self.request.user)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # Update the items manually if using checkboxes in the template
        selected_items = self.request.POST.getlist('items')
        self.object.items.set(selected_items)
        return response

    def get_success_url(self):
        return self.object.get_absolute_url()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(username=instance)

@login_required
def remove_friend(request, pk):
    friend_profile = get_object_or_404(Profile, pk=pk)
    
    # Get the current user's profile
    try:
        user_profile = Profile.objects.get(username=request.user)
    except Profile.DoesNotExist:
        # Redirect if user doesn't have a profile
        return redirect('project:profile_list')
    
    # Remove the friendship by deleting the Friend object
    # Check both directions since friendship can be stored either way
    Friend.objects.filter(
        (models.Q(profile1=user_profile, profile2=friend_profile) |
         models.Q(profile1=friend_profile, profile2=user_profile))
    ).delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'project:profile_list'))

class DeleteOutfitView(LoginRequiredMixin, DeleteView):
    model = Outfit
    template_name = 'project/confirm_delete_outfit.html'
    success_url = reverse_lazy('project:my_profile')

    def get_queryset(self):
        # Only allow deleting outfits owned by the current user
        return Outfit.objects.filter(profile__username=self.request.user)

class DebugLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        print(f"DEBUG: User after login: {self.request.user}, is_authenticated: {self.request.user.is_authenticated}")
        return response

def my_login_view(request):
    if request.method == 'POST':
        print("DEBUG: Login POST request received")
        username = request.POST['username']
        password = request.POST['password']
        print(f"DEBUG: Attempting login for username: {username}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(f"DEBUG: Authentication successful for user: {user}")
            login(request, user)
            print(f"DEBUG: User is_authenticated: {request.user.is_authenticated}")
            print(f"DEBUG: request.user: {request.user}")
            # ... redirect or render ...
        else:
            print("DEBUG: Authentication failed")
            # ... handle error ...
    # ... rest of view ...

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'city', 'email', 'bio', 'profile_image']
    template_name = 'project/edit_profile.html'
    success_url = reverse_lazy('project:my_profile')

    def get_object(self):
        return Profile.objects.get(username=self.request.user)