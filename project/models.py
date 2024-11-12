from django.db import models

class Cause(models.Model):
    cuase_title = models.TextField()
    social_cause_categories = models.TextField()
    # related_causes = models.TextField()

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
    
class Product(models.Model):
    '''Store/represent the data relating to one specific product'''
    product_name = models.TextField()
    product_category = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    nutritional_info = models.TextField()
    nutritional_score = models.IntegerField()

    environmental_info = models.TextField()
    environmental_score = models.IntegerField()

    ethical_info = models.TextField()
    ethical_score = models.IntegerField()

    associated_causes = models.ManyToManyField(Cause)

    def __str__(self):
        '''Return a string representation of this product instance.'''
        return f'{self.product_name} is a {self.product_category} product by {self.brand}.'
    
    def get_similar_products(self):
        # get similar products
        return
    
    def get_better_products(self):
        # get similar products with better scores
        return

class Figures(models.Model):
    '''Stores/represents data related to a figure, such as an image or graph'''
    # image_url or imageField

def load_data():
    '''initial loading of data into django database, most popular products.'''

def update_data():
    '''Adds a new instance tinot database via API lookup OR user entry, triggered when user searches for an unrecognized product'''
