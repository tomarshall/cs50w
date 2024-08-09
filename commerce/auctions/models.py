from django.contrib import admin
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max

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
    current_highest_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_highest_bidder = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="highest_bids")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="selling")
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="won_auctions")

    def update_highest_bid(self):
        highest_bid = self.bids.order_by('-amount').first()
        if highest_bid:
            self.current_highest_bid = highest_bid.amount
            self.current_highest_bidder = highest_bid.bidder
        else:
            self.current_highest_bid = self.starting_bid
            self.current_highest_bidder = None
        self.save()

    def highest_bid(self):
        highest_bid = self.bids.order_by('-amount').first()
        return highest_bid.amount if highest_bid else self.starting_bid
    
    def save(self, *args, **kwargs):
        if self.current_highest_bid is None:
            self.current_highest_bid = self.starting_bid
        super().save(*args, **kwargs)

    def close_auction(self):
        self.active = False
        self.winner = self.current_highest_bidder
        self.save()

    def __str__(self):
        return self.title


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.listing.update_highest_bid()
        self.listing.save()

    class Meta:
        ordering = ['-amount']

    def __str__(self):
        return f"{self.bidder.username} bid ${self.amount} on {self.listing.title}"


class Comment(models.Model):
    pass
