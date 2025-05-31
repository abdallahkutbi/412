from django import forms
from .models import Profile, StatusMessage

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





    
