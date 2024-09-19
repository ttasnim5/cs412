# quotes/views.py
from django.shortcuts import render
import random

quotes = [
    "“Neither love nor terror makes one blind: indifference makes one blind.” - <i>If Beale Street Could Talk</i>",
    "“The victim who is able to articulate the situation of the victim has ceased to be a victim: he or she has become a threat.” - <i>The Devil Finds Work</i>",
    "“Please try to remember that what they believe, as well as what they do and cause you to endure does not testify to your inferiority but to their inhumanity.” - <i>The First Next Time</i>",
    "“To be a Negro in this country and to be relatively conscious is to be in a rage almost all the time.” - a 1961 radio interview",
    "“Those who say it can’t be done are usually interrupted by others doing it.” - <i>Notes of a Native Son</i>",
    "“The most dangerous creation of any society is the man who has nothing to lose.” - <i>The Fire Next Time</i>",
    "“Not everything that is faced can be changed, but nothing can be changed until it is faced.” - <i>No Name in the Street</i>",
    "“Everybody’s journey is individual. If you fall in love with a boy, you fall in love with a boy. The fact that many Americans consider it a disease says more about them than it does about homosexuality.” - <i>Conversations with James Baldwin</i>",
    "“There are so many ways of being despicable it quite makes one’s head spin. But the way to be really despicable is to be contemptuous of other people’s pain.” - <i>Giovanni’s Room</i>",
    "“If one really wishes to know how justice is administered in a country, one does not question the policemen, the lawyers, the judges, or the protected members of the middle class. One goes to the unprotected – those, precisely, who need the law’s protection most! – and listens to their testimony.” - <i>No Name in the Street</i>",
    "“Anyone who has ever struggled with poverty knows how extremely expensive it is to be poor.” - <i>Nobody Knows My Name</i>",
    "“You think your pain and your heartbreak are unprecedented in the history of the world, but then you read.” - an 1963 interview in LIFE magazine",
]

images = [
    "/static/jbaldwin1.jpg",
    "/static/jbaldwin2.jpg",
    "/static/jbaldwin3.jpg",
    "/static/jbaldwin4.jpg",
    "/static/jbaldwin5.jpg",
    "/static/jbaldwin6.jpg",
    "/static/jbaldwin7.jpg",
    "/static/jbaldwin8.jpg",
    "/static/jbaldwin9.jpg",
    "/static/jbaldwin10.jpg",
    "/static/jbaldwin11.jpg",
    "/static/jbaldwin12.jpg",
]

def quote(request):
    context = {
        'quote': random.choice(quotes),
        'image': random.choice(images),
    }
    return render(request, 'quotes/home.html', context)

def show_all(request):
    # Zip quotes and images together for easier iteration in the template
    quotes_and_images = list(zip(quotes, images))
    context = {
        'quotes_and_images': quotes_and_images,
    }
    return render(request, 'quotes/show_all.html', context)

def about(request):
    return render(request, 'quotes/about.html')
