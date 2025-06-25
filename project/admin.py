from django.contrib import admin

# Register your models here.

from .models import Profile, Outfit, Friend, ProfileImage, OutfitImage, OutfitItem

# Only register Outfit for admin management

admin.site.register(Profile)
admin.site.register(OutfitItem)
admin.site.register(Outfit)
admin.site.register(Friend)
admin.site.register(ProfileImage)
admin.site.register(OutfitImage)

