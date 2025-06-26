"""
Forms for the Project application.
This module defines the forms used in the application, including forms for creating profiles and outfits.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Outfit, OutfitItem

class CreateProfileForm(forms.ModelForm):
    '''
    A form to create a new profile
    '''
    first_name = forms.CharField(label="First Name", required=True, max_length=100)
    last_name = forms.CharField(label="Last Name", required=True, max_length=100)
    city = forms.CharField(label="City", required=True, max_length=100)
    email = forms.EmailField(label="Email", required=True)
    bio = forms.CharField(label="Bio", required=False, widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about your fashion style...'}))
    profile_image = forms.ImageField(label="Profile Image", required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'bio', 'profile_image']

class CreateOutfitForm(forms.ModelForm):
    '''
    A form to create a new outfit
    '''
    subject = forms.CharField(label="Outfit Name", required=True, max_length=200, 
                             widget=forms.TextInput(attrs={'placeholder': 'e.g., Summer Casual Look'}))
    # items field will be set in the view to filter by user if needed

    class Meta:
        model = Outfit
        fields = ['subject', 'items']

class CreateOutfitItemForm(forms.ModelForm):
    '''
    A form to create a new clothing item
    '''
    name = forms.CharField(label="Item Name", required=True, max_length=100)
    item_type = forms.ChoiceField(label="Item Type", required=True, choices=OutfitItem.ITEM_TYPES)
    image = forms.ImageField(label="Item Image", required=True)
    price = forms.DecimalField(label="Price ($)", required=True, min_value=0, decimal_places=2)
    brand = forms.CharField(label="Brand", required=True, max_length=100)

    class Meta:
        model = OutfitItem
        fields = ['name', 'item_type', 'image', 'price', 'brand']

class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ['subject']  # or any other fields you want for the outfit

class OutfitItemForm(forms.ModelForm):
    class Meta:
        model = OutfitItem
        fields = ['name', 'item_type', 'image', 'price', 'brand']