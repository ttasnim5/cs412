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

def analyze_causes(product_data):
    """Infer causes for a product based on its data."""
    inferred_causes = []

    # Environmental Impact
    ecoscore = product_data.get("ecoscore_grade", "").lower()
    if ecoscore in ["a", "b"]:
        environmental_cause, _ = Cause.objects.get_or_create(
            title="Eco-Friendly Product",
            category="Environmental Impact",
            defaults={"description": "Product has a high ecoscore grade (A or B)."}
        )
        inferred_causes.append(environmental_cause)

    if all(ingredient.get("vegan") == "yes" for ingredient in product_data.get("ingredients", [])):
        vegan_cause = Cause.objects.get_or_create(
            title="Vegan Product",
            category="Animal Welfare",
            defaults={"description": "The product is vegan-friendly, with no animal-derived ingredients."}
        )[0]
        inferred_causes.append(vegan_cause)

    if all(ingredient.get("vegetarian") == "yes" for ingredient in product_data.get("ingredients", [])):
            vegetarian_cause = Cause.objects.get_or_create(
                title="Vegetarian Product",
                category="Animal Welfare",
                defaults={"description": "The product is vegetarian-friendly, with no non-vegetarian ingredients."}
            )[0]
            inferred_causes.append(vegetarian_cause)

    # Health & Nutrition
    if product_data.get("nutriments", {}).get("nutrition_score_fr_100g", 0) <= 2:
        healthy_cause, _ = Cause.objects.get_or_create(
            title="Healthy Choice",
            category="Health & Nutrition",
            defaults={"description": "Low nutrition score indicates a healthier product."}
        )
        inferred_causes.append(healthy_cause)

    # Ethical Marketing
    if "organic" in product_data.get("categories_tags", []):
        organic_cause, _ = Cause.objects.get_or_create(
            title="Certified Organic",
            category="Ethical Marketing",
            defaults={"description": "The product is certified organic, promoting ethical sourcing and marketing."}
        )
        inferred_causes.append(organic_cause)

    return inferred_causes

def get_data():
    Product.objects.all().delete()
    Cause.objects.all().delete()
    NutritionalInfo.objects.all().delete()
    EnvironmentalInfo.objects.all().delete()
    Brand.objects.all().delete()

    num_products = 100
    base_url = "https://world.openfoodfacts.org/cgi/search.pl"

    for page in range(1, (num_products // 100) + 1):
        response = requests.get(base_url, params={
            'action': 'process',
            'sort_by': 'popularity',
            'page_size': 100,
            'page': page,
            'json': True
        })

        if response.status_code != 200:
            print(f"Error fetching data for page {page}")
            break

        data = response.json()
        products = data.get('products', [])

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
                    # update product categories for brand
                    if not brand.product_categories:
                        brand.product_categories = product_data['categories']
                        brand.save()
                    prod.brands.add(brand)

            # infer and associate causes
            causes = analyze_causes(product)
            prod.causes.add(*causes)

            print(f"Created Product: {prod.product_name} with {len(causes)} causes.")
