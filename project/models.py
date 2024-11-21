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
        return f'{self.title} centers the topics: {self.category}.'
    
class Brand(models.Model):
    '''Store/represent the data relating to one brand'''
    brand_name = models.CharField(max_length=255, unique=True)  # unique to prevent duplicates
    product_categories = models.TextField(null=True, blank=True)
    help_causes = models.ManyToManyField(Cause, blank=True)  # causes supported by the brand

    def __str__(self):
        return f'{self.brand_name}'

class EnvironmentalInfo(models.Model):
    carbon_footprint_100g = models.IntegerField(null=True, blank=True, default=0)
    ecoscore_grade = models.TextField(null=True, blank=True, default="N/A")
    packaging = models.TextField(null=True, blank=True, default="N/A")
    production_system = models.TextField(null=True, blank=True, default="N/A")
    epi_score = models.IntegerField(null=True, blank=True, default=0)  # 0-100

    def __str__(self):
        # use reverse access to get the product name, it is inherently efficient in most use cases
        product = getattr(self, 'product', None)  # Reverse relation to Product
        product_name = product.product_name if product else "Unknown Product"
        return f"{product_name} (Ecoscore: {self.ecoscore_grade})"


class NutritionalInfo(models.Model):
    energy_kcal_100g = models.IntegerField(null=True, blank=True, default=0)
    proteins_100g = models.IntegerField(null=True, blank=True, default=0)
    carbohydrates_100g = models.IntegerField(null=True, blank=True, default=0)
    fat_100g = models.IntegerField(null=True, blank=True, default=0)
    nutrition_grade_fr = models.CharField(max_length=3, null=True, blank=True, default="N/A")

    def __str__(self):
        return f"Nutritional Info (Grade: {self.nutrition_grade_fr})"


class Product(models.Model):
    product_name = models.TextField(default="N/A")
    code = models.TextField(default="N/A")
    categories = models.TextField(null=True, blank=True, default="N/A")
    categories_tags = models.TextField(null=True, blank=True, default="N/A")
    brands = models.ManyToManyField(Brand, related_name="products")  # Link to Brand model
    brands_tags = models.TextField(null=True, blank=True, default="N/A")
    origins = models.TextField(null=True, blank=True, default="N/A")
    manufacturing_places = models.TextField(null=True, blank=True, default="N/A")
    countries = models.TextField(null=True, blank=True, default="N/A")
    main_category = models.TextField(null=True, blank=True, default="N/A")
    ingredients_text = models.TextField(null=True, blank=True, default="N/A")
    traces = models.TextField(null=True, blank=True, default="N/A")

    nutritional_info = models.OneToOneField(
        NutritionalInfo, null=True, blank=True, on_delete=models.CASCADE
    )
    environmental_info = models.OneToOneField(
        EnvironmentalInfo, null=True, blank=True, on_delete=models.CASCADE
    )
    causes = models.ManyToManyField(Cause, blank=True)

    def __str__(self):
        brand_names = ", ".join([brand.brand_name for brand in self.brands.all()]) or "Unknown Brand"
        return f"{self.product_name} by {brand_names}"

###################################################################################
def get_data():
    num_products = 15000
    page_size = 1000
    base_url = "https://world.openfoodfacts.org/cgi/search.pl"

    Product.objects.all().delete()
    Cause.objects.all().delete()
    NutritionalInfo.objects.all().delete()
    EnvironmentalInfo.objects.all().delete()
    Brand.objects.all().delete()

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
            # Nutritional Info
            nutritional_data = {
                'energy_kcal_100g': product.get('nutriments', {}).get('energy-kcal_100g', 0),
                'proteins_100g': product.get('nutriments', {}).get('proteins_100g', 0),
                'carbohydrates_100g': product.get('nutriments', {}).get('carbohydrates_100g', 0),
                'fat_100g': product.get('nutriments', {}).get('fat_100g', 0),
                'nutrition_grade_fr': product.get('nutrition_grade_fr', '').upper(),
            }
            nutritional_info = NutritionalInfo(**nutritional_data)
            nutritional_info.save()

            # Environmental Info
            environmental_data = {
                'carbon_footprint_100g': product.get('nutriments', {}).get('carbon-footprint_100g', 0),
                'ecoscore_grade': product.get('ecoscore_grade'),
                'packaging': product.get('ecoscore_data', {}).get('adjustments', {}).get('packaging', {}),
                'production_system': product.get('ecoscore_data', {}).get('adjustments', {}).get('production_system', {}),
                'epi_score': product.get('ecoscore_data', {}).get('adjustments', {}).get('origins_of_ingredients', {}).get('epi_score', {}),
            }
            environmental_info = EnvironmentalInfo(**environmental_data)
            environmental_info.save()

            # Product Data
            product_data = {
                'product_name': product.get('product_name', '').replace('\n', ' ').replace('\r', ' '),
                'code': product.get('code', ''),
                'categories': product.get('categories', '').replace('\n', ' ').replace('\r', ' '),
                'categories_tags': str(product.get('categories_tags', '')),
                'origins': product.get('origins', '').replace('\n', ' ').replace('\r', ' '),
                'manufacturing_places': product.get('manufacturing_places', '').replace('\n', ' ').replace('\r', ' '),
                'countries': product.get('countries', '').replace('\n', ' ').replace('\r', ' '),
                'main_category': product.get('main_category', '').replace('\n', ' ').replace('\r', ' '),
                'ingredients_text': product.get('ingredients_text', '').replace('\n', ' ').replace('\r', ' '),
                'traces': product.get('traces', '').replace('\n', ' ').replace('\r', ' '),
                'nutritional_info': nutritional_info,
                'environmental_info': environmental_info,
            }
            prod = Product(**product_data)
            prod.save()

            # Brand Association
            brand_names = product.get('brands', '').split(',')
            brand_objects = []
            for brand_name in brand_names:
                brand_name = brand_name.strip()
                if brand_name:
                    brand, _ = Brand.objects.get_or_create(brand_name=brand_name)
                    brand_objects.append(brand)
                    # Update product categories for brand
                    if not brand.product_categories:
                        brand.product_categories = product_data['categories']
                        brand.save()
                    prod.brands.add(brand)

            # Cause Analysis for Product
            causes = []
            if nutritional_info.nutrition_grade_fr in ['A', 'B']:
                cause, _ = Cause.objects.get_or_create(
                    title="High Nutritional Quality",
                    category="Health & Nutrition",
                    defaults={"description": "The product has a high nutrition score."}
                )
                causes.append(cause)
                prod.causes.add(cause)

            if environmental_info.ecoscore_grade in ['a', 'a-plus', 'b']:
                cause, _ = Cause.objects.get_or_create(
                    title="Eco-Friendly",
                    category="Environmental Impact",
                    defaults={"description": "The product is environmentally sustainable."}
                )
                causes.append(cause)
                prod.causes.add(cause)

            # Assign Causes to Brands
            for cause in causes:
                for brand in brand_objects:
                    brand.help_causes.add(cause)

            print(f'Created product: {prod.product_name}')

        if len(products) < page_size:
            print("End of available products reached.")
            break

    print(f'Done. Created {Product.objects.count()} Products, {Brand.objects.count()} Brands, and associated Causes.')
