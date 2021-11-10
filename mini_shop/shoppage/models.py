from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField('product_name', max_length=100, default='Товар')
    description = models.TextField('description', default='ProductDescription')
    price = models.IntegerField('price', default=0)
    type = models.CharField('type', max_length=30)
    weight = models.IntegerField('weight')

    def __str__(self):
        return self.name

