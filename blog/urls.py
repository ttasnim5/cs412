## blog/urls.py
## description: the app-specific URLS for the blog application

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views ## NEW
from . import views

# create a list of URLs for this app:
urlpatterns = [
    # path(url, view, name)
    path(r'', views.RandomArticleView.as_view(), name="random"), 
    path(r'show_all', views.ShowAllView.as_view(), name="show_all"), 
    path(r'article/<int:pk>', views.ArticleView.as_view(), name="article"), 
    #path(r'create_comment', views.CreateCommentView.as_view(), name="create_comment"), 
    path(r'article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name="create_comment"),
    path(r'create_article', views.CreateArticleView.as_view(), name="create_article"),
    path('register/', views.RegistrationView.as_view(), name='register'),

    # authentication URLs:
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'),
           name='login'), ## NEW
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), 
         name='logout'), ## NEW
]
