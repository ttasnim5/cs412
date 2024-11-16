from django.db import models
import requests

class Cause(models.Model):
    title = models.CharField(max_length=255)  # Specific cause title
    category = models.CharField(
        max_length=50,
        choices=[
            ("Environmental Impact", "Environmental Impact"),
            ("Labor Practices", "Labor Practices"),
            ("Animal Welfare", "Animal Welfare"),
            ("Health & Nutrition", "Health & Nutrition"),
            ("Ethical Marketing", "Ethical Marketing"),
            ("Community Support", "Community Support"),
        ],
    )
    description = models.TextField(null=True, blank=True)  # Optional for details about the cause


    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.cause_title} centers the topics: {self.social_cause_categories}.'
    
    def related_causes(self):
        return 
    
    def helpful_companies(self):
        '''Known companies that aid this cause'''
        return
    
    def harmful_companies(self):
        '''Known companies that harm this cause'''
        return    
    
class Brand(models.Model):
    '''Store/represent the data relating to one brand'''
    brand_name = models.TextField()
    product_categories = models.TextField()
    help_causes = models.ManyToManyField(Cause)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.brand_name} specializes in: {self.product_categories}.'
    
class Figures(models.Model):
    '''Stores/represents data related to a figure, such as an image or graph'''
    # image_url or imageField

class Product(models.Model):
    product_name = models.TextField(default="N/A")
    code = models.TextField(default="N/A")
    categories = models.TextField(null=True, blank=True, default="N/A")
    categories_tags = models.TextField(null=True, blank=True, default="N/A")
    brands = models.TextField(null=True, blank=True, default="N/A")
    brands_tags = models.TextField(null=True, blank=True, default="N/A")
    origins = models.TextField(null=True, blank=True, default="N/A")
    manufacturing_places = models.TextField(null=True, blank=True, default="N/A")
    countries = models.TextField(null=True, blank=True, default="N/A")
    nutrition_grade_fr = models.CharField(max_length=3, null=True, blank=True, default="N/A")
    main_category = models.TextField(null=True, blank=True, default="N/A")
    ingredients_text = models.TextField(null=True, blank=True, default="N/A")
    traces = models.TextField(null=True, blank=True, default="N/A")
    energy_kcal_100g = models.IntegerField(null=True, blank=True, default=0)
    proteins_100g = models.IntegerField(null=True, blank=True, default=0)
    carbohydrates_100g = models.IntegerField(null=True, blank=True, default=0)
    fat_100g = models.IntegerField(null=True, blank=True, default=0)
    carbon_footprint_100g = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        '''Return a string representation of this Product instance.'''
        return f'{self.product_name} by {self.brands}'

###################################################################################
def get_data():
    num_products = 15000
    page_size = 1000
    base_url = "https://world.openfoodfacts.org/cgi/search.pl"

    Product.objects.all().delete()

    for page in range(1, num_products // page_size + 1):
        response = requests.get(base_url, params={
            'action': 'process',
            'sort_by': 'popularity',
            'page_size': page_size,
            'page': page,
            'json': True
        })

        if response.status_code != 200:
            print(f"Error: Failed to retrieve data on page {page}")
            break

        data = response.json()
        products = data.get('products', [])

        if not products:
            print("No more products found; ending data retrieval.")
            break

        for product in products:

            row = {
                'product_name': product.get('product_name', '').replace('\n', ' ').replace('\r', ' '),
                'code': product.get('code', ''),
                'categories': product.get('categories', '').replace('\n', ' ').replace('\r', ' '),
                'categories_tags': str(product.get('categories_tags', '')),
                'brands': product.get('brands', '').replace('\n', ' ').replace('\r', ' '),
                'brands_tags': str(product.get('brands_tags', '')),
                'origins': product.get('origins', '').replace('\n', ' ').replace('\r', ' '),
                'manufacturing_places': product.get('manufacturing_places', '').replace('\n', ' ').replace('\r', ' '),
                'countries': product.get('countries', '').replace('\n', ' ').replace('\r', ' '),
                'nutrition_grade_fr': product.get('nutrition_grade_fr', '').upper(),
                'main_category': product.get('main_category', '').replace('\n', ' ').replace('\r', ' '),
                'ingredients_text': product.get('ingredients_text', '').replace('\n', ' ').replace('\r', ' '),
                'traces': product.get('traces', '').replace('\n', ' ').replace('\r', ' '),
                'energy_kcal_100g': product.get('nutriments', {}).get('energy-kcal_100g', 0),
                'proteins_100g': product.get('nutriments', {}).get('proteins_100g', 0),
                'carbohydrates_100g': product.get('nutriments', {}).get('carbohydrates_100g', 0),
                'fat_100g': product.get('nutriments', {}).get('fat_100g', 0),
                'carbon_footprint_100g': product.get('nutriments', {}).get('carbon-footprint_100g', 0),
            }

            prod = Product(**row)
            prod.save()
            print(f'Created product: {prod.product_name}')

        if len(products) < page_size:
            print("End of available products reached.")
            break

    print(f'Done. Created {Product.objects.count()} Products.')