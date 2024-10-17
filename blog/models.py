# blog/models.py
# Define data models (objects) for use in the blog application
from django.db import models
from django.urls import reverse


# Create your models here.
class Article(models.Model):
    '''Encapsulate the data for a blog Article by some author.'''

    # data attributes:
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    # image_url = models.URLField(blank=True) ## new field
    image_file = models.ImageField(blank=True)

    def __str__(self):
        '''Return a string representation of this Article.'''
        return f"{self.title} by {self.author}"
    
    def get_comments(self):
        '''Retrieve all comments for this Article.'''

        # use the ORM to filter Comments where this 
        # instance of Article is the FK
        comments = Comment.objects.filter(article=self)
        return comments

    def get_absolute_url(self):
        '''Return the URL to display this Article.'''
        return reverse('article', kwargs={'pk':self.pk})


class Comment(models.Model):
    '''Encapsulate a comment on an article.'''

    # create a 1 to many relationship between Articles and Comments
    article = models.ForeignKey("Article", on_delete=models.CASCADE) ### IMPORTANT
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this object.'''
        return f'{self.text}'
    