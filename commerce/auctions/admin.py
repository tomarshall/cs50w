from django.contrib import admin

from .models import Category, Listing

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ["title", "starting_bid", "category", "created_at", "last_updated"]


admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)