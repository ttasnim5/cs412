## write the CreateCommentForm
# blog/forms.py
from django import forms
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
    class Meta: # meta meaning information about the form
        '''associate this form with the Comment model; select fields.'''
        model = Comment
        # fields = ['article', 'author', 'text', ]  # which fields from model should we use
        fields = ['author', 'text', ]  # which fields from model should we use