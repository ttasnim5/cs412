# marathon_analytics/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views 

urlpatterns = [
    # map the URL (empty string) to the view
    path(r'', views.ProductsListView.as_view(), name='home'),
    path(r'nutrition_results', views.ProductsByNutritionView.as_view(), name='nutrition_results'),
    path(r'env_impact_results', views.ProductsByEnvImpactView.as_view(), name='env_impact_results'),
    path(r'product/<int:pk>', views.ProductDetailView.as_view(), name='product'),
    path(r'product_graph/<int:pk>', views.ProductGraphsDetailView.as_view(), name='product_graph'),
    path(r'product/create', views.CreateProductView.as_view(), name='create_product'),    
    path(r'product/update/<int:pk>', views.UpdateProductView.as_view(), name='update_product'),    
    path(r'product/delete/<int:pk>', views.DeleteProductView.as_view(), name='delete_product'),
    path(r'brand/<int:pk>', views.ShowBrandPageView.as_view(), name='show_brand'),
    path(r'cause/<int:pk>', views.ShowCausePageView.as_view(), name='show_cause'),
    path(r'cause/category/<int:pk>/', views.ShowCauseCategoryView.as_view(), name='cause_category'),
    path(r'cause_list', views.CauseListView.as_view(), name='cause_list'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]