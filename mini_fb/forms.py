from django import forms
from .models import Profile, StatusMessage

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a Status Message to the database.'''
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), max_length=280, label='')

    class Meta: # meta meaning information about the form
        '''associate this form with the SM model; select fields.'''
        model = StatusMessage
        fields = ['message', ]  # which fields from model should we use

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database.'''

    class Meta: # meta meaning information about the form
        '''associate this form with the Profile model; select fields.'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image_url',]  

        widgets = {
            'first_name': forms.Textarea(attrs={'rows': 1}),
            'last_name': forms.Textarea(attrs={'rows': 1}),
            'city': forms.Textarea(attrs={'rows': 1}),
            'email': forms.Textarea(attrs={'rows': 1}),
            'image_url': forms.Textarea(attrs={'rows': 1}),
        }

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a Profile in the database.'''

    class Meta: # meta meaning information about the form
        '''associate this form with the Profile model; select fields.'''
        model = Profile
        fields = ['city', 'email', 'image_url',]  

        widgets = {
            'city': forms.Textarea(attrs={'rows': 1}),
            'email': forms.Textarea(attrs={'rows': 1}),
            'image_url': forms.Textarea(attrs={'rows': 1}),
        }

class UpdateStatusMessageForm(forms.ModelForm):
    '''A form to update a Status Message in the database.'''
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), max_length=280, label='')

    class Meta: # meta meaning information about the form
        '''associate this form with the SM model; select fields.'''
        model = StatusMessage
        fields = ['message', ]  # which fields from model should we use