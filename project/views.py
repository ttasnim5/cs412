from collections import Counter
from django.shortcuts import redirect
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from . models import *

import plotly
import plotly.graph_objs as go

# todo list: separate out the origins, manufacture places, ingredients, categories
# make buttons smaller ??
# restrict size of display and make table cols evenly spaced
# make the product information "click for more"
   
class ProductsListView(ListView):
    '''View to display product results'''
    template_name = 'project/home.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 25

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

        if product_name:
            qs = qs.filter(product_name__icontains=product_name)
        if brands:
            qs = qs.filter(brands__brand_name__icontains=brands)
        if categories:
            qs = qs.filter(categories__icontains=categories)
        if origins:
            qs = qs.filter(origins__icontains=origins)
        if nutrition_grade_fr:
            qs = qs.filter(nutritional_info__nutrition_grade_fr=nutrition_grade_fr)
        if ingredients:
            qs = qs.filter(ingredients_text__icontains=ingredients)
        if energy_kcal_100g:
            qs = qs.filter(nutritional_info__energy_kcal_100g__gte=energy_kcal_100g)
        if proteins_100g:
            qs = qs.filter(nutritional_info__proteins_100g__gte=proteins_100g)
        if carbohydrates_100g:
            qs = qs.filter(nutritional_info__carbohydrates_100g__gte=carbohydrates_100g)
        if fat_100g:
            qs = qs.filter(nutritional_info__fat_100g__gte=fat_100g)
        if carbon_footprint_100g:
            qs = qs.filter(environmental_info__carbon_footprint_100g__gte=carbon_footprint_100g)
        
        return qs
    
class ProductDetailView(DetailView):
    '''View to show detail page for one product.'''
    template_name = 'project/product.html'
    model = Product
    context_object_name = 'p'
    
class ProductGraphsDetailView(DetailView):
    '''View to show detail page for one product.'''
    template_name = 'project/product_graph.html'
    model = Product
    context_object_name = 'p'

    def get_context_data(self, **kwargs):
        '''Provide context variables for use in template.'''
        context = super().get_context_data(**kwargs)
        p = context.get('p')

        # ensure product has valid macronutrient data
        if p.nutritional_info.carbohydrates_100g !=0 and p.nutritional_info.fat_100g !=0 and p.nutritional_info.proteins_100g !=0:
            x = ['Carbohydrates (g per 100g)', 'Fats (g per 100g)', 'Proteins (g per 100g)']
            y = [p.nutritional_info.carbohydrates_100g, p.nutritional_info.fat_100g, p.nutritional_info.proteins_100g]
            
            fig = go.Figure(data=[go.Pie(labels=x, values=y)])
            fig.update_layout(
                title_text="Macronutrient Breakdown",
                colorway=["#D8DBBD", "#003161", "#AF1740"]
            )
            macro_distribution_graph = plotly.offline.plot(fig, auto_open=False, output_type="div")
            context['macro_distribution_graph'] = macro_distribution_graph
        else: # handle missing data
            context['macro_distribution_graph'] = "<p>Graphical macronutrient data not displayed for this product.</p>"

        # extract and clean location data
        origins = p.origins.split(",") if p.origins else []
        manufacturing_places = p.manufacturing_places.split(",") if p.manufacturing_places else []
        countries = p.countries.split(",") if p.countries else []

        # create the figure
        fig = go.Figure()

        # plot origins
        if origins:
            fig.add_trace(go.Scattergeo(
                locations=origins,
                locationmode="country names",
                marker=dict(color="blue", size=8, symbol="circle"),
                name="Origins"
            ))

        # plot places of manufacture
        if manufacturing_places:
            fig.add_trace(go.Scattergeo(
                locations=manufacturing_places,
                locationmode="country names",
                marker=dict(color="green", size=8, symbol="square"),
                name="Manufacturing Places"
            ))

        # plot countries of distribution
        if countries:
            fig.add_trace(go.Scattergeo(
                locations=countries,
                locationmode="country names",
                marker=dict(color="red", size=8, symbol="triangle-up"),
                name="Countries of Distribution"
            ))

        fig.update_layout(
            title_text="Geographical Data for Product",
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type="equirectangular"
            ),
            legend=dict(
                title="Key",
                x=0.9, y=0.9
            )
        )

        geo_graph = plotly.offline.plot(fig, auto_open=False, output_type="div")
        context['geo_graph'] = geo_graph if (origins or manufacturing_places or countries) else "<p>Geographical data not available for this product.</p>"
        
        if p.nutritional_info.nutrition_grade_fr:
            grade = p.nutritional_info.nutrition_grade_fr.upper()
            grade_value = ord(grade) - ord('A') + 1
            color_mapping = { 'A': 'darkgreen', 'B': 'lightgreen', 'C': 'yellow', 'D': 'orange', 'E': 'red' }
            bar_color = color_mapping.get(grade, 'gray')  # default to gray if grade is invalid
        else: # defaults/unknown values
            grade_value = 0  

        # create the gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=grade_value,
            gauge={
                "axis": {
                    "range": [0, 5],
                    "tickvals": [0, 1, 2, 3, 4, 5],
                    "ticktext": ["", "A", "B", "C", "D", "E"]
                },
                "bar": {"color": bar_color}
            }
        ))

        fig.update_layout(title_text="Nutrition Grade")

        nutrition_grade_graph = plotly.offline.plot(fig, auto_open=False, output_type="div")
        context['nutrition_grade_graph'] = nutrition_grade_graph if (p.nutritional_info.nutrition_grade_fr) else "<p>Nutrition Grading data not available for this product.</p>"
        
        fig = go.Figure(go.Indicator(mode="number+gauge", value=p.environmental_info.carbon_footprint_100g,
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "green" if p.environmental_info.carbon_footprint_100g <= 50 else "red"}
            }
        ))
        fig.update_layout(title_text="Carbon Footprint (g CO₂ per 100g)")
        carbon_graph = plotly.offline.plot(fig, auto_open=False, output_type="div")
        context['carbon_graph'] = carbon_graph if (p.environmental_info.carbon_footprint_100g >= 0) else "<p>Environmental comparative data not displayed for this product.</p>"
        
        return context
    
class ProductsByNutritionView(ListView):
    '''View to display product results by nutrition grade'''
    template_name = 'project/nutrition_results.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by('nutritional_info__nutrition_grade_fr')

class ProductsByEnvImpactView(ListView):
    '''View to display product results by nutrition grade'''
    template_name = 'project/env_impact_results.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        # this currently returns a > a+, need to FIX + capitalize
        return qs.order_by('environmental_info__ecoscore_grade')
    
class CauseListView(ListView):
    '''View to display product results by nutrition grade'''
    # put an arder by __ checkbox option on these
    template_name = 'project/cause_list.html'
    model = Cause
    context_object_name = 'causes'
    paginate_by = 25

class ShowBrandPageView(DetailView):
    '''Displays the detail of a specific cause by their primary key'''
    model = Brand  # specifies which model to use for this view
    template_name = 'project/show_brand.html'  
    context_object_name = 'brand'  # name to use for the profile object in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = self.get_object()  # get the current object
        products = brand.products.all()
        # related_name="products" overrides the default reverse accessor (product_set) with products
        context['products'] = products 
        return context

class ShowCausePageView(DetailView):
    '''Displays the detail of a specific cause by their primary key'''
    model = Cause  # specifies which model to use for this view
    template_name = 'project/show_cause.html'  
    context_object_name = 'cause'  # name to use for the profile object in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cause = self.get_object()  # get the current cause object
        products = cause.product_set.all()  # retrieve all products associated with this cause
        context['products'] = products 
        return context
    
class ShowCauseCategoryView(DetailView):
    '''Displays all products associated with a cause category.'''
    model = Cause
    template_name = 'project/cause_category.html'
    context_object_name = 'cause'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cause = self.get_object()  # current cause object
        # get all products linked to causes in the same category
        related_causes = Cause.objects.filter(category=cause.category)
        products = Product.objects.filter(causes__in=related_causes).distinct()
        context['products'] = products
        context['category'] = cause.category
        return context
    
    # product page: 
    #   + comparison tab (products similar nutritionally, environmentally)
