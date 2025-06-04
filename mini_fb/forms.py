from django import forms
from .models import Profile, StatusMessage, Image

class CreateProfileForm(forms.ModelForm):
    '''
    A form to create a new profile
    '''
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    email = forms.EmailField(label="Email", required=True)
    image = forms.ImageField(label="Profile Image", required=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image']


class CreateStatusMessageForm(forms.ModelForm):
    '''
    A form to create a new status message
    '''
    message = forms.CharField(label="Status Message", required=True)
    class Meta:
        model = StatusMessage
        fields = ['message']   


class CreateImageForm(forms.ModelForm):
    '''
    A form to create a new image
    '''
    image_file = forms.ImageField(label="Image", required=True)
    caption = forms.CharField(label="Caption", required=True)

    class Meta:
        model = Image
        fields = ['image_file', 'caption']

class UpdateProfileForm(forms.ModelForm):
    '''
    A form to update a profile
    '''
    city = forms.CharField(label="City", required=False)
    email = forms.EmailField(label="Email", required=False)

    class Meta:
        model = Profile
        fields = ['city', 'email']

    