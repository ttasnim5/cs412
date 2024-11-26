# marathon_analytics/urls.py
from django.urls import path
from . import views 

urlpatterns = [
    # map the URL (empty string) to the view
    path(r'', views.ProductsListView.as_view(), name='home'),
    path(r'nutrition_results', views.ProductsByNutritionView.as_view(), name='nutrition_results'),
    path(r'env_impact_results', views.ProductsByEnvImpactView.as_view(), name='env_impact_results'),
    path(r'product/<int:pk>', views.ProductDetailView.as_view(), name='product'),
    path(r'cause_results', views.ProductsByEnvCauseView.as_view(), name='cause_results'),
]