"""
Models for the Mini Facebook application.
This module defines the database models used in the application, including
Profile, StatusMessage, Image, StatusImage, and Friend models.
"""

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    '''
    Profile model
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile', null=True)
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    image_url = models.TextField(blank=True)
    
    def get_status_messages(self):
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        """Returns the URL to access a particular profile instance."""
        return reverse('show_profile', kwargs={'pk': self.pk})

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
        Returns a QuerySet of status messages from this profile and all friends,
        ordered by most recent first.
        """
        friend_profiles = self.get_friends()
        
        return StatusMessage.objects.filter(
            profile__in=list(friend_profiles) + [self]
        ).order_by('-timestamp')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Image(models.Model):
    '''
    Image model
    '''
    image_file = models.ImageField(upload_to='profile_images/')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.first_name} {self.profile.last_name} at {self.timestamp}"
    
    def get_absolute_url(self):
        return reverse('show_image', kwargs={'pk': self.pk})
    
    def get_image_url(self):
        return self.image_file.url
  

class StatusImage(models.Model):
    '''
    Links StatusMessages to Images
    '''
    status_message = models.ForeignKey('StatusMessage', on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.status_message.profile.first_name}"


class StatusMessage(models.Model):
    '''
    Status message model
    '''
    message = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile.first_name} {self.profile.last_name} at {self.timestamp}"
    
    def get_status_messages(self):
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_images(self):
        return StatusImage.objects.filter(status_message=self)

class Friend(models.Model):
    '''
    Friend model to represent friendships between profiles
    '''
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"