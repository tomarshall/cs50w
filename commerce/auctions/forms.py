from django import forms
from django.core.exceptions import ValidationError
from .models import Listing, Category, Bid

class CreateListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        to_field_name="category",
        empty_label="Select a category"
    )

    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_url", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "starting_bid": forms.NumberInput(attrs={"class": "form-control"}),
            "image_url": forms.URLInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].widget.attrs.update({"class": "form-select"})


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(attrs={"step": "0.01", "min": "0.01"})
        }
    
    # The contructor method for the form
    def __init__(self, *args, **kwargs):
        # Looks for a "listing" key in the `kwargs` dictionary.
        # If found, it removes ('pops') this key-value pair from `kwargs` and assigns the value self.listing
        # If not found, it assigns `None` to self.listing
        self.listing = kwargs.pop("listing", None)
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if not self.listing:
            raise ValidationError("Listing is required")
        
        highest_bid = self.listing.bids.order_by("-amount").first()

        if highest_bid:
            if amount <= highest_bid.amount:
                raise ValidationError(f"Bid must be higher than ${highest_bid.amount}")
        else:
            if amount <= self.listing.starting_bid:
                raise ValidationError(f"Bid must be higher than the starting bid of ${self.listing.starting_bid}")
        
        return amount
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.listing = self.listing
        instance.bidder = self.user
        if commit:
            instance.save()
        return instance