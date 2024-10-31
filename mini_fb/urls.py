from django.urls import path
from . import views
from django.contrib.auth import views as auth_views ## NEW

urlpatterns = [
    path('', views.ShowAllView.as_view(), name="show_all_profiles"),
    path('show_all', views.ShowAllView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', views.ShowProfilePageView.as_view(), name='show_profile'),
    path('create_new_profile/<int:user_id>/', views.CreateProfilePageView.as_view(), name='create_new_profile'),    path('profile/<int:pk>/update', views.UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name='update_status'),
    path('profile/<int:pk>/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name='add_friend'),
    path('profile/<int:pk>/friend_suggestions', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/<int:pk>/news_feed', views.ShowNewsFeedView.as_view(), name='news_feed'),
    # authentication URLs:
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'), ## NEW
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_profiles'), name='logout'), ## NEW
    path('register/', views.RegistrationView.as_view(), name="register"), ## NEW

]
