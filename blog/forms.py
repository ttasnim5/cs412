# blog/forms.py

from django import forms
from .models import Comment, Article

class CreateCommentForm(forms.ModelForm):
    '''A form to create Comment data.'''

    class Meta:
        '''associate this form witht he Comment model'''
        model = Comment
        # fields = ['article', 'author', 'text', ]
        # remove the article because we want to do this automagically
        fields = ['author', 'text', ]

class CreateArticleForm(forms.ModelForm):
    '''A form to create a new Article.'''

    class Meta:
        '''Associate this form with a Model, specify which fields to create.'''
        model = Article
        fields = ['author', 'title', 'text', 'image_file']