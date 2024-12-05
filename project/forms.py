from django import forms
from .models import Product, Cause, Brand, NutritionalInfo, EnvironmentalInfo

class NutritionalInfoForm(forms.ModelForm):
    class Meta:
        model = NutritionalInfo
        fields = ['energy_kcal_100g', 'proteins_100g', 'carbohydrates_100g', 'fat_100g', 'nutrition_grade_fr']
        widgets = {field: forms.Textarea(attrs={'rows': 1}) for field in fields}

class EnvironmentalInfoForm(forms.ModelForm):
    class Meta:
        model = EnvironmentalInfo
        fields = ['carbon_footprint_100g', 'ecoscore_grade', 'packaging', 'production_system', 'epi_score']
        widgets = {field: forms.Textarea(attrs={'rows': 1}) for field in fields}
        
class CreateProductForm(forms.ModelForm):
    '''A form to add a Product to the database.'''
    
    causes = forms.ModelMultipleChoiceField(
        queryset=Cause.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    brands = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        widget=forms.SelectMultiple,
        required=False
    )
    
    class Meta:
        model = Product
        fields = [
            'product_name', 'code', 'main_category', 'categories', 'categories_tags', 'brands', 'brands_tags',
            'ingredients_text', 'origins', 'manufacturing_places', 'countries', 'causes',
        ]

        widgets = {
            'product_name': forms.Textarea(attrs={'rows': 1}),
            'code': forms.Textarea(attrs={'rows': 1}),
            'main_category': forms.Textarea(attrs={'rows': 1}),
            'categories': forms.Textarea(attrs={'rows': 1}),
            'categories_tags': forms.Textarea(attrs={'rows': 1}),
            'ingredients_text': forms.Textarea(attrs={'rows': 1}),
            'origins': forms.Textarea(attrs={'rows': 1}),
            'manufacturing_places': forms.Textarea(attrs={'rows': 1}),
            'countries': forms.Textarea(attrs={'rows': 1}),
            'epi_score': forms.Textarea(attrs={'rows': 1}),
        }

