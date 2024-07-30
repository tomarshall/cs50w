from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models


# Category i.e. Fashion, Toys, Electronics, Home, etc.
class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_url = models.URLField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    pass


class Comment(models.Model):
    pass
