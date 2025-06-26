"""
Models for the Project application.
This module defines the database models used in the application, including
Profile, Outfit, and Friend models.
"""

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    '''
    Profile model
    '''
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_profile', null=True, blank=True)
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    image_url = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name},{self.username}"
    
    def get_outfits(self):
        return Outfit.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        """Returns the URL to access a particular profile instance."""
        return reverse('project:profile_detail', kwargs={'pk': self.pk})

    def get_friends(self):
        """
        Returns a list of all friends' profiles for this profile.
        """
        friends1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        friend_ids = list(friends1) + list(friends2)
        return Profile.objects.filter(id__in=friend_ids)

    def add_friend(self, other):
        """
        Add a friend relationship between this profile and another profile.
        Prevents self-friending and duplicate friendships.
        """
        if self == other:
            return False
        
        if Friend.objects.filter(profile1=self, profile2=other).exists() or \
           Friend.objects.filter(profile1=other, profile2=self).exists():
            return False
        
        Friend.objects.create(profile1=self, profile2=other)
        return True

    def get_friend_suggestions(self):
        """
        Returns a list of profiles that could be suggested as friends.
        Excludes current friends and self.
        """
        current_friends = self.get_friends().values_list('id', flat=True)
        
        suggestions = Profile.objects.exclude(
            id__in=list(current_friends) + [self.id]
        )
        
        return suggestions

    def get_news_feed(self):
        """
        Returns a QuerySet of outfits from this profile and all friends,
        ordered by most recent first.
        """
        friend_profiles = self.get_friends()
        
        return Outfit.objects.filter(
            profile__in=list(friend_profiles) + [self]
        ).order_by('-timestamp')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class OutfitItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ITEM_TYPES = [
        ('shirt', 'Shirt'),
        ('pants', 'Pants'),
        ('shoes', 'Shoes'),
        ('accessory', 'Accessory'),
        ('dress', 'Dress'),
        ('jacket', 'Jacket'),
        ('hat', 'Hat'),
        ('bag', 'Bag'),
    ]
    name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    image = models.ImageField(upload_to='outfit_images/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Outfit(models.Model):
    '''
    Outfit model - like StatusMessage but for outfits
    '''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    items = models.ManyToManyField(OutfitItem)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    
    def total_price(self):
        return sum(item.price for item in self.items.all())

    def __str__(self):
        return self.subject
    
    def get_absolute_url(self):
        """Returns the URL to access a particular outfit instance."""
        return reverse('project:outfit_detail', kwargs={'pk': self.pk})


class Friend(models.Model):
    '''
    Friend model to represent friendships between profiles
    '''
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1', null=True)
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2', null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.profile1 and self.profile2:
            return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"
        return "Invalid friendship"


class ProfileImage(models.Model):
    '''
    Image model
    '''
    image_file = models.ImageField(upload_to='outfit_images/')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

class OutfitImage(models.Model):
    '''
    Image model
    '''
    image_file = models.ImageField(upload_to='outfit_images/')
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
