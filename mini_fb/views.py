from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
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
        form = CreateStatusMessageForm(request.POST, request.FILES)  # create a form instance with the submitted data
        
        if form.is_valid():
            status_message = form.save(commit=False)  # create a new StatusMessage object
            status_message.profile = self.object  # add new status message to profile
            status_message.save()  # save the status message to the database
            
            # handle the image files
            files = self.request.FILES.getlist('files')  # get the list of uploaded files (images)
            for file in files:
                image = Image()  # create a new Image object
                image.message = status_message  # set the ForeignKey to the status message
                image.image_file = file  # assign the file to the ImageField
                image.save()  # save the Image object to the database

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
    
class UpdateProfileView(UpdateView):
    model = Profile 
    form_class = UpdateProfileForm  # form class to use for updating profiles
    template_name = 'mini_fb/update_profile_form.html'  

    def form_valid(self, form):
        # this is called when valid form data has been POSTed
        self.object = form.save()  # save the new profile to the database
        return redirect('show_profile', pk=self.object.pk)  # redirect to the newly created profile's page
    
class DeleteStatusMessageView(DeleteView):
    model = StatusMessage 
    template_name = 'mini_fb/delete_status_form.html'  
    context_object_name = 'status_message'  # name to use for the sm object in the template

    def get_success_url(self): # redirect to the profile page after deletion
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class UpdateStatusMessageView(UpdateView):
    model = StatusMessage 
    form_class = UpdateStatusMessageForm  # form class to use for updating sm's
    template_name = 'mini_fb/update_status_form.html'  
    context_object_name = 'status_message'

# when do we need to override the post method ?
    def form_valid(self, form): # this is called when valid form data has been POSTed
        self.object = form.save()  # save the new profile to the database
    
        if form.is_valid(): # handle the image files
            files = self.request.FILES.getlist('files')  # get the list of uploaded files (images)
            for file in files:
                image = Image()  # create a new Image object
                image.message = self.object  # set the ForeignKey to the status message
                image.image_file = file  # assign the file to the ImageField
                image.save()  # save the Image object to the database

            return redirect('show_profile', pk=self.object.profile.pk)  # redirect to the profile page
        else:
            return self.render_to_response(self.get_context_data(form=form))  # re-render the page with the form errors
    

class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        # extract profile1 (p1) and profile2 (p2) from the URL parameters
        p1 = get_object_or_404(Profile, pk=self.kwargs['pk'])
        p2 = get_object_or_404(Profile, pk=self.kwargs['other_pk'])

        p1.add_friend(p2)
        # redirect to p1's profile page after creating the friendship
        return redirect('show_profile', pk=p1.pk)

class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'  # context for the user's profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()  
        user_friends = profile.get_friends()

        mutuals = set()  # set to avoid duplicates
        for friend in user_friends:
            mutuals.update(set(friend.get_friends()) - {profile})

        context['profiles'] = list(mutuals)
        context['user'] = profile
        return context
