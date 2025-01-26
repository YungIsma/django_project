from django.conf import settings
from django.db import models
from django.utils import timezone

class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    descriptoin = models.TextField()
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")  # Поле для загрузки изображений
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

