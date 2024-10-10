from . models import *
from . forms import *
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
import random

class ShowAllView(ListView):
    '''A view to show all Articles'''
    model = Article
    template_name = 'blog/all.html'
    context_object_name = 'articles'
    
class RandomArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
    # specify the object to show:
    def get_object(self):
        '''Return one Article object chosen at random.'''
        all_articles = Article.objects.all()
        return random.choice(all_articles)

class ArticleView(DetailView):
    '''show one particle by primary key'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

## write the CreateCommentView
from .forms import CreateCommentForm
class CreateCommentView(CreateView):
    '''A view to create a new comment and save it to the database.
    On GET: sends back the form
    On POST: read the form data, create an instance of Comment, save to database
    '''
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def form_valid(self, form):
        '''
        Handle the form submission. We need to set the foreign key by 
        attaching the Article to the Comment object.
        We can find the article PK in the URL (self.kwargs).
        '''
        print(form.cleaned_data)
        article = Article.objects.get(pk=self.kwargs['pk'])
        # print(article)
        form.instance.article = article
        return super().form_valid(form)
    
        ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        # return "/blog/all"
        # return reverse('all')
        return reverse('article', kwargs={'pk': self.kwargs['pk']})
