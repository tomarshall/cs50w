from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Listing, User, Bid, Comment, Upvote

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ["title", "seller", "starting_bid", "current_highest_bidder", "current_highest_bid", "category", "created_at", "active"]


class BidAdmin(admin.ModelAdmin):
    list_display = ["listing_title", "bidder_username", "amount", "timestamp"]
    
    def listing_title(self, obj):
        return obj.listing.title
    listing_title.short_description = 'Listing'
    
    def bidder_username(self, obj):
        return obj.bidder.username
    bidder_username.short_description = 'Bidder'


admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(Upvote)