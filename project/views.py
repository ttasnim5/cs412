from django.db.models import Case, When, Value, CharField
from django.shortcuts import redirect, render
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic import View, ListView, DetailView, UpdateView, DeleteView
from . models import *
from . forms import *

import plotly
import plotly.graph_objs as go

# todo list: add navbar, separate out and translate the origins, manufacture places, ingredients, categories
   
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
        ecoscore = self.request.GET.get('ecoscore', '').strip()
        ingredients = self.request.GET.get('ingredients', '')

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
        if ecoscore:
            qs = qs.filter(environmental_info__ecoscore_grade=ecoscore)
        if ingredients:
            qs = qs.filter(ingredients_text__icontains=ingredients)

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
        
        invalid_values = ['n/a', 'N/A', 'not-applicable', 'NOT-APPLICABLE', 'unknown', 'UNKNOWN', None]

        # check if the ecoscore is valid (not in the invalid_values list)
        ecoscore = str(p.environmental_info.ecoscore_grade).strip()

        if ecoscore == "a-plus" or ecoscore == "A-PLUS":
            ecoscore = "A+"  # special case for A+
            grade_value = 1  # assign a value higher than "A" (e.g., A+ = 1.5)
            bar_color = 'darkgreen'  # special color for "A+"
        else:
            if ecoscore not in invalid_values and len(ecoscore) == 1:
                grade = ecoscore.upper()
                if grade == "A":
                    grade_value = 1  # Regular "A"
                    bar_color = 'mediumgreen'
                elif grade == "B":
                    grade_value = 2
                    bar_color = 'lightgreen'
                elif grade == "C":
                    grade_value = 3
                    bar_color = 'yellow'
                elif grade == "D":
                    grade_value = 4
                    bar_color = 'orange'
                elif grade == "E":
                    grade_value = 5
                    bar_color = 'red'
                elif grade == "F":
                    grade_value = 6
                    bar_color = 'darkred'
                else:
                    grade_value = 0
                    bar_color = 'gray'
            else:
                grade_value = 0
                bar_color = 'gray'

        fig = go.Figure(go.Indicator(
            mode="gauge+number", 
            value=grade_value,
            gauge={
                "axis": {
                    "range": [0, 6],
                    "tickvals": [0, 1, 2, 3, 4, 5, 6, 7],
                    "ticktext": ["", "A+", "A", "B", "C", "D", "E", "F"]
                },
                "bar": {"color": bar_color}
            }
        ))
        fig.update_layout(title_text="Ecoscore Grade")
        ecoscore_graph = plotly.offline.plot(fig, auto_open=False, output_type="div")

        # add the graph to the context if the ecoscore is valid
        if ecoscore not in invalid_values:
            context['ecoscore_graph'] = ecoscore_graph
        else:
            context['ecoscore_graph'] = "<p>Ecoscore data not displayed for this product.</p>"

        return context


class UpdateProductView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'project/update_product.html'
    context_object_name = 'p'
    fields = [
        'product_name', 'categories', 'origins', 'manufacturing_places', 'countries',
        'ingredients_text', 'traces', 'nutritional_info', 'environmental_info', 'causes'
    ]  # base fields in your Product model

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pass the ecoscore choices as a list
        context = super().get_context_data(**kwargs)
        # pass the choices for ecoscore and nutrition grades
        context['ecoscore_choices'] = ['a-plus', 'a', 'b', 'c', 'd', 'e', 'f']
        context['nutrition_grade_choices'] = ['A', 'B', 'C', 'D', 'E']
        context['causes'] = Cause.objects.all()
        return context
    
    def form_valid(self, form):
        product = form.save(commit=False)
        # Update related models here

        # Update Brands
        brands_input = self.request.POST.get('brands', '')
        if brands_input:
            brand_names = [name.strip() for name in brands_input.split(',')]
            product.brands.clear()
            for brand_name in brand_names:
                brand, _ = Brand.objects.get_or_create(brand_name=brand_name)
                product.brands.add(brand)

        # Update Nutritional Info
        nutritional_data = {
            'energy_kcal_100g': self.request.POST.get('energy_kcal_100g'),
            'proteins_100g': self.request.POST.get('proteins_100g'),
            'carbohydrates_100g': self.request.POST.get('carbohydrates_100g'),
            'fat_100g': self.request.POST.get('fat_100g'),
            'nutrition_grade_fr': self.request.POST.get('nutrition_grade_fr'),
        }
        if product.nutritional_info:
            for field, value in nutritional_data.items():
                setattr(product.nutritional_info, field, value)
            product.nutritional_info.save()
        else:
            nutritional_info = NutritionalInfo.objects.create(**nutritional_data)
            product.nutritional_info = nutritional_info

        # Update Environmental Info
        environmental_data = {
            'carbon_footprint_100g': self.request.POST.get('carbon_footprint_100g'),
            'ecoscore_grade': self.request.POST.get('ecoscore'),
        }
        if product.environmental_info:
            for field, value in environmental_data.items():
                setattr(product.environmental_info, field, value)
            product.environmental_info.save()
        else:
            environmental_info = EnvironmentalInfo.objects.create(**environmental_data)
            product.environmental_info = environmental_info

        causes_ids = self.request.POST.getlist('causes')  # get selected causes as a list
        causes = Cause.objects.filter(pk__in=causes_ids)  # fetch the Cause objects
        self.object.causes.set(causes)  # update the product's causes

        product.save()
        return redirect(product.get_absolute_url())

class ProductsByNutritionView(ListView):
    '''View to display product results by nutrition grade'''
    template_name = 'project/nutrition_results.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        
        # order by nutrition grade with NULL, "unknown", and "N/A" values at the end
        qs = qs.annotate(
            nutrition_grade_order=Case(
                When(nutritional_info__nutrition_grade_fr__in=['unknown', 'n/a','UNKNOWN', 'NOT-APPLICABLE', 'N/A',None], then=Value(999)),
                When(nutritional_info__nutrition_grade_fr='A', then=Value(1)),
                When(nutritional_info__nutrition_grade_fr='B', then=Value(2)),
                When(nutritional_info__nutrition_grade_fr='C', then=Value(3)),
                When(nutritional_info__nutrition_grade_fr='D', then=Value(4)),
                When(nutritional_info__nutrition_grade_fr='E', then=Value(5)),
                default=Value(999),
                output_field=CharField()
            )
        ).order_by('nutrition_grade_order')
        
        return qs

class ProductsByEnvImpactView(ListView):
    '''View to display product results by environmental impact (ecoscore)'''
    template_name = 'project/env_impact_results.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        
        # order by ecoscore grade with "A+" always first and unknown values last
        qs = qs.annotate(
            ecoscore_order=Case(
                When(environmental_info__ecoscore_grade__in=['unknown', 'n/a','UNKNOWN', 'NOT-APPLICABLE', 'N/A',None], then=Value(999)),
                When(environmental_info__ecoscore_grade='a-plus', then=Value(1)),  # "A+" ranked first
                When(environmental_info__ecoscore_grade='a', then=Value(2)),
                When(environmental_info__ecoscore_grade='b', then=Value(3)),
                When(environmental_info__ecoscore_grade='c', then=Value(4)),
                When(environmental_info__ecoscore_grade='d', then=Value(5)),
                When(environmental_info__ecoscore_grade='e', then=Value(6)),
                When(environmental_info__ecoscore_grade='f', then=Value(7)),
                default=Value(999),
                output_field=CharField()
            )
        ).order_by('ecoscore_order')
        
        return qs
    
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
    context_object_name = 'brand'  # name to use for the product object in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = self.get_object()  # get the current object
        products = brand.products.all()
        # related_name="products" overrides the default reverse accessor (product_set) with products
        # add num products, possibly a search for products ?
        context['products'] = products 
        return context

class ShowCausePageView(DetailView):
    '''Displays the detail of a specific cause by their primary key'''
    model = Cause  # specifies which model to use for this view
    template_name = 'project/show_cause.html'  
    context_object_name = 'cause'  # name to use for the product object in the template

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
    
class DeleteProductView(LoginRequiredMixin, DeleteView):
    '''Displays and processes form to delete a specific product'''
    model = Product 
    template_name = 'project/delete_product.html'  
    context_object_name = 'product'  # name to use for the  object in the template

    def get_success_url(self): # redirect to the product page after deletion
        return reverse('home')

class CreateProductView(View):
    def get(self, request):
        product_form = CreateProductForm()
        nutritional_form = NutritionalInfoForm()
        environmental_form = EnvironmentalInfoForm()
        return render(request, 'project/create_product.html', {
            'product_form': product_form,
            'nutritional_form': nutritional_form,
            'environmental_form': environmental_form,
        })

    def post(self, request):
        product_form = CreateProductForm(request.POST)
        nutritional_form = NutritionalInfoForm(request.POST)
        environmental_form = EnvironmentalInfoForm(request.POST)

        if product_form.is_valid() and nutritional_form.is_valid() and environmental_form.is_valid():
            nutritional_info = nutritional_form.save()
            environmental_info = environmental_form.save()
            product = product_form.save(commit=False)
            product.nutritional_info = nutritional_info
            product.environmental_info = environmental_info
            product.save()
            product_form.save_m2m()  # save Many-to-Many relationships
            return redirect('product', pk=product.pk)

        return render(request, 'project/create_product.html', {
            'product_form': product_form,
            'nutritional_form': nutritional_form,
            'environmental_form': environmental_form,
        })