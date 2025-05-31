from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''
    Profile model
    '''
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    image = models.ImageField(upload_to='profile_images/')

    def get_status_messages(self):
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        """Returns the URL to access a particular profile instance."""
        return reverse('show_profile', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    





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

  