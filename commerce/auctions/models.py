from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    pass


class Bid(models.Model):
    pass


class Comment(models.Model):
    pass


# Category i.e. Fashion, Toys, Electronics, Home, etc.
class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"