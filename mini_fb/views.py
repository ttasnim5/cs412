from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import redirect
from .models import *
from .forms import *

class ShowAllView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile  # specifies which model to use for this view
    template_name = 'mini_fb/show_profile.html'  
    context_object_name = 'profile'  # name to use for the profile object in the template

    def get_context_data(self, **kwargs):
        # add extra context data to the template
        context = super().get_context_data(**kwargs)  # get default context data
        context['form'] = CreateStatusMessageForm()  # add an empty form for new status messages
        return context

    def post(self, request, *args, **kwargs):
        # handles POST requests (i.e., form submissions)
        self.object = self.get_object()  # get profile object
        form = CreateStatusMessageForm(request.POST)  # create a form instance with the submitted data
        if form.is_valid():
            status_message = form.save(commit=False)  # create a new StatusMessage object
            status_message.profile = self.object  # add new status message to profile
            status_message.save()  # save the status message to the database
            return redirect('show_profile', pk=self.object.pk)  # redirect to the profile page
        else:
            return self.render_to_response(self.get_context_data(form=form))  # re-render the page with the form errors
        

class CreateProfilePageView(CreateView):
    model = Profile 
    form_class = CreateProfileForm  # form class to use for creating profiles
    template_name = 'mini_fb/create_profile_form.html'  

    def form_valid(self, form):
        # this is called when valid form data has been POSTed
        self.object = form.save()  # save the new profile to the database
        return redirect('show_profile', pk=self.object.pk)  # redirect to the newly created profile's page