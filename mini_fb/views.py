from django.shortcuts import render
from . models import *
from django.views.generic import ListView

class ShowAllView(ListView):
    '''A view to show all Articles'''
    model = Profile
    template_name = 'mini_fb/show_all.html'
    context_object_name = 'profiles'
    