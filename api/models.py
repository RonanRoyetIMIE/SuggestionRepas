from django.db import models
from django.contrib.auth.models import User

class User(User):
    pass

class Product(models.Model):
    user_id = models.CharField(max_length=255, blank=False, default='', unique=False)

    code = models.CharField(max_length=255, blank=False, default='', unique=False)
    
    sub_code = models.CharField(max_length=255, blank=False, default='', unique=False)

    brands = models.CharField(max_length=255, blank=False, default='', unique=False)
        
    keywords = models.CharField(max_length=4095, blank=False, default='', unique=False)

    categories_tags = models.CharField( max_length=4095, blank=False, default='', unique=False)

    countries = models.CharField(max_length=4095, blank=False, default='', unique=False)

    ingredients_text = models.CharField(max_length=4095, blank=False, default='', unique=False)

    image_url = models.CharField(max_length=255, blank=False, default='', unique=False)
