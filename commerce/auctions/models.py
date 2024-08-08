from django.contrib import admin
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

import datetime


# Category i.e. Fashion, Toys, Electronics, Home, etc.
class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watched_by")

    def __str__(self):
        return self.username


class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_url = models.URLField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-amount']

    def __str__(self):
        return f"{self.bidder.username} bid ${self.amount} on {self.listing.title}"


class Comment(models.Model):
    pass
