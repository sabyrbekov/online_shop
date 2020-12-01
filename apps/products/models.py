from django.db import models
from apps.category.models import (
    Category, Brand
)
from django.contrib.auth import get_user_model
from apps.authentication.models import AbstractEmailUser
User = get_user_model()

class ProductModel(models.Model):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='brand', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title


class Wish(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product} --> {self.user}'
