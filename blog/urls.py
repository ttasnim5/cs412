# blog/urls.py
from django.urls import path
from .views import * # our view class definition 
urlpatterns = [
    # map the URL (empty string) to the view
    path('', RandomArticleView.as_view(), name='random'),
    path('all', ShowAllView.as_view(), name='all'), 
    path('article/<int:pk>', ArticleView.as_view(), name='article'), 
    # path('create_comment', CreateCommentView.as_view(), name='create_comment'),
    path('article/<int:pk>/create_comment', ArticleView.as_view(), name='article'), 
]