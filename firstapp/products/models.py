from django.db import models

class Product(models.Model):
    title = models.TextField()
    price = models.TextField()
    description = models.TextField()