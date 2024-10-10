from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShowAllView.as_view(), name="show_all_profiles"),
    path('show_all', views.ShowAllView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', views.ShowProfilePageView.as_view(), name='show_profile'),
    path('create_new_profile', views.CreateProfilePageView.as_view(), name='create_new_profile'),
]