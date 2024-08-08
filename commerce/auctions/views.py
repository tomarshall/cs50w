from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .forms import CreateListingForm, BidForm
from .models import User, Category, Listing


def create_listing(request):
    if request.method == "POST":
        # Create a form instance with the submitted data
        form = CreateListingForm(request.POST)
        # Check if form data is valid
        if form.is_valid():
            # Saves form (creating a new Listing object)
            form.save()
            return redirect("index")
    else:
        # Create empty form
        form = CreateListingForm()

    # Render template with the form
    return render(request, "auctions/create_listing.html", {
        "form": form,
    })


def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    is_watching = listing in request.user.watchlist.all()
    form = BidForm(listing=listing, user=request.user)

    if request.method == "POST":
        if "watchlist" in request.POST:
            if is_watching:
                request.user.watchlist.remove(listing)
            else:
                request.user.watchlist.add(listing)
            return redirect(reverse("listing_detail", args=[listing_id]))
        
        if "bid" in request.POST:
            form = BidForm(request.POST, listing=listing, user=request.user)
            if form.is_valid():
                form.save()
                return redirect("listing_detail", listing_id=listing.id)

    context = {
        "listing": listing,
        "is_watching": is_watching,
        "form": form,
        "highest_bid": listing.highest_bid()
    }
    return render(request, "auctions/listing_detail.html", context)


@login_required
def watchlist(request):
    watchlist_items = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {"watchlist_items": watchlist_items})


def index(request):
    listings = Listing.objects.all().order_by("-created_at")
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
