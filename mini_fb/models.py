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
    image_url = models.TextField(blank=True)
    
    def get_status_messages(self):
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        """Returns the URL to access a particular profile instance."""
        return reverse('show_profile', kwargs={'pk': self.pk})

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

