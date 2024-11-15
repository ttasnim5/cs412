from collections import Counter
from django.shortcuts import render
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from . models import *

class ProductsListView(ListView):
    '''View to display voter results'''
    template_name = 'project/home.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset()

        product_name = self.request.GET.get('product_name', '').strip()
        brands = self.request.GET.get('brands', '').strip()
        categories = self.request.GET.get('categories', '').strip()
        origins = self.request.GET.get('origins', '').strip()
        nutrition_grade_fr = self.request.GET.get('nutrition_grade_fr', '')
        ingredients = self.request.GET.get('ingredients', '').strip()
        energy_kcal_100g = self.request.GET.get('energy_kcal_100g', '').strip()
        proteins_100g = self.request.GET.get('proteins_100g', '').strip()
        carbohydrates_100g = self.request.GET.get('carbohydrates_100g', '').strip()
        fat_100g = self.request.GET.get('fat_100g', '').strip()
        carbon_footprint_100g = self.request.GET.get('carbon_footprint_100g', '').strip()

        # Apply filters conditionally
        if product_name:
            qs = qs.filter(product_name__icontains=product_name)
        if brands:
            qs = qs.filter(brands__icontains=brands)
        if categories:
            qs = qs.filter(categories__icontains=categories)
        if origins:
            qs = qs.filter(origins__icontains=origins)
        if nutrition_grade_fr:
            qs = qs.filter(nutrition_grade_fr=nutrition_grade_fr)
        if ingredients:
            qs = qs.filter(ingredients_text__icontains=ingredients)
        if energy_kcal_100g:
            qs = qs.filter(energy_kcal_100g__gte=energy_kcal_100g)
        if proteins_100g:
            qs = qs.filter(proteins_100g__gte=proteins_100g)
        if carbohydrates_100g:
            qs = qs.filter(carbohydrates_100g__gte=carbohydrates_100g)
        if fat_100g:
            qs = qs.filter(fat_100g__gte=fat_100g)
        if carbon_footprint_100g:
            qs = qs.filter(carbon_footprint_100g__gte=carbon_footprint_100g)
        
        return qs
    
class ProductDetailView(DetailView):
    '''View to show detail page for one result.'''
    template_name = 'project/product.html'
    model = Product
    context_object_name = 'p'