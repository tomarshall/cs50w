from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse

from .forms import CreateListingForm, BidForm, CommentForm
from .models import User, Listing, Comment, Category


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})


def category_detail(request, category_id):
    # Get the category or return a 404 if not found
    category = get_object_or_404(Category, id=category_id)
    
    # Get all active listings in this category
    listings = Listing.objects.filter(category=category).order_by('-created_at')

    # Pagination (not important -- just for when there's more listings)
    paginator = Paginator(listings, 10) # Show 10 listings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "category": category,
        "page_obj": page_obj,
        "listings": page_obj,
    }
    return render(request, "auctions/category_detail.html", context)


@login_required
def create_listing(request):
    if request.method == "POST":
        # Create a form instance with the submitted data
        form = CreateListingForm(request.POST)
        # Check if form data is valid
        if form.is_valid():
            # Saves form (creating a new Listing object)
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
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

    if request.user.is_authenticated:
        is_watching = listing in request.user.watchlist.all()
        is_owner = request.user == listing.seller
        is_winner = request.user.is_authenticated and listing.winner == request.user
    else:
        is_watching = False
        is_owner = False
        is_winner = False
    
    comments = listing.comments.all()
    
    bid_form = BidForm(listing=listing, user=request.user)
    comment_form = CommentForm()

    if request.method == "POST":
        if "watchlist" in request.POST:
            if is_watching:
                request.user.watchlist.remove(listing)
            else:
                request.user.watchlist.add(listing)
            return redirect(reverse("listing_detail", args=[listing_id]))
        
        if "bid" in request.POST:
            bid_form = BidForm(request.POST, listing=listing, user=request.user)
            if bid_form.is_valid():
                bid = bid_form.save()
                messages.success(request, f"Your bid of ${bid.amount} was placed successfully.")
                return redirect("listing_detail", listing_id=listing.id)
        
        if "close_auction" in request.POST and is_owner and listing.active:
            listing.close_auction()
            messages.success(request, "Auction closed successfully.")
            return redirect("listing_detail", listing_id=listing_id)
        
        if "comment" in request.POST and request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.listing = listing
                comment.user = request.user
                comment.save()
                messages.success(request, "Your comment has been posted.")
                return redirect("listing_detail", listing_id=listing_id)
        
        if "upvote" in request.POST:
            comment_id = request.POST.get("comment_id")
            comment = get_object_or_404(Comment, id=comment_id)
            comment.upvotes += 1
            comment.save()
            messages.success(request, "Comment upvoted.")
            return redirect("listing_detail", listing_id=listing_id)

    context = {
        "listing": listing,
        "is_active": listing.active,
        "is_watching": is_watching,
        "bid_form": bid_form,
        "highest_bid": listing.highest_bid(),
        "is_owner": is_owner,
        "is_winner": is_winner,
        "comments": comments,
        "comment_form": comment_form
    }
    return render(request, "auctions/listing_detail.html", context)


@login_required
def watchlist(request):
    watchlist_items = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {"watchlist_items": watchlist_items})


def index(request):
    listings = Listing.objects.all().order_by("-created_at")
    return render(request, "auctions/index.html", {"listings": listings,})


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
