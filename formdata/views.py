## formdata/views.py 
## get the form to display as "main" web page for this app:
from django.shortcuts import render, redirect
# Create your views here.
def show_form(request):
    '''Show the web page with the form.'''
    template_name = "formdata/show_form.html"
    return render(request, template_name)

def submit(request):
    '''Handle form submission, read out data, generate response.'''
    template_name = "formdata/confirmation.html"
    print(request)

    # check for POST vs GET
    if request.POST:
        #  read data into python variables
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']

        #  package them up to be used in the response
        context = {
            'name': name,
            'favorite_color': favorite_color,
        }
        return render(request, template_name, context)
    
    # GET  lands down here
    template_name = 'formdata/show_form.html'
    return redirect("show_form")
