# marathon_analytics/urls.py
from django.urls import path
from . import views 

urlpatterns = [
    # map the URL (empty string) to the view
    path(r'', views.ProductsListView.as_view(), name='home'),
    path(r'nutrition_results', views.ProductsByNutritionView.as_view(), name='nutrition_results'),
    path(r'env_impact_results', views.ProductsByEnvImpactView.as_view(), name='env_impact_results'),
    path(r'product/<int:pk>', views.ProductDetailView.as_view(), name='product'),
    path(r'product_graph/<int:pk>', views.ProductGraphsDetailView.as_view(), name='product_graph'),
    path(r'product/update/<int:pk>', views.UpdateProductView.as_view(), name='update_product'),    
    path(r'brand/<int:pk>', views.ShowBrandPageView.as_view(), name='show_brand'),
    path(r'cause/<int:pk>', views.ShowCausePageView.as_view(), name='show_cause'),
    path(r'cause/category/<int:pk>/', views.ShowCauseCategoryView.as_view(), name='cause_category'),
    path(r'cause_list', views.CauseListView.as_view(), name='cause_list'),
]