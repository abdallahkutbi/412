from django.db import models

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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

  