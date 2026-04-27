from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import BidForm, CommentForm, ListingForm
from .models import Bid, Category, Listing, User


def index(request):
    listings = Listing.objects.select_related("owner", "category").filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/login.html", {
            "message": "Invalid username and/or password."
        })

    return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            messages.success(request, "Listing created successfully.")
            return redirect("listing_detail", listing_id=listing.id)
    else:
        form = ListingForm()

    return render(request, "auctions/create_listing.html", {
        "form": form,
    })


def listing_detail(request, listing_id):
    listing = get_object_or_404(
        Listing.objects.select_related("owner", "category", "winner"),
        id=listing_id,
    )

    is_watchlisted = False
    if request.user.is_authenticated:
        is_watchlisted = listing.watchlist.filter(id=request.user.id).exists()

    comments = listing.comments.select_related("commenter")
    highest_bid = listing.highest_bid

    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "highest_bid": highest_bid,
        "is_watchlisted": is_watchlisted,
        "bid_form": BidForm(),
        "comment_form": CommentForm(),
        "comments": comments,
    })


@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method != "POST":
        return redirect("listing_detail", listing_id=listing.id)

    if listing.watchlist.filter(id=request.user.id).exists():
        listing.watchlist.remove(request.user)
        messages.success(request, "Removed from your watchlist.")
    else:
        listing.watchlist.add(request.user)
        messages.success(request, "Added to your watchlist.")

    return redirect("listing_detail", listing_id=listing.id)


@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method != "POST":
        return redirect("listing_detail", listing_id=listing.id)

    if not listing.active:
        messages.error(request, "This auction is already closed.")
        return redirect("listing_detail", listing_id=listing.id)

    if listing.owner == request.user:
        messages.error(request, "You cannot bid on your own listing.")
        return redirect("listing_detail", listing_id=listing.id)

    form = BidForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Please enter a valid bid amount.")
        return redirect("listing_detail", listing_id=listing.id)

    amount = form.cleaned_data["amount"]

    if amount < listing.starting_bid:
        messages.error(request, "Your bid must be at least the starting bid.")
        return redirect("listing_detail", listing_id=listing.id)

    highest_bid = listing.highest_bid
    if highest_bid and amount <= highest_bid.amount:
        messages.error(request, "Your bid must be greater than the current highest bid.")
        return redirect("listing_detail", listing_id=listing.id)

    Bid.objects.create(
        listing=listing,
        bidder=request.user,
        amount=amount,
    )
    messages.success(request, "Your bid was placed successfully.")
    return redirect("listing_detail", listing_id=listing.id)


@login_required
def close_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method != "POST":
        return redirect("listing_detail", listing_id=listing.id)

    if listing.owner != request.user:
        messages.error(request, "Only the listing owner can close this auction.")
        return redirect("listing_detail", listing_id=listing.id)

    if not listing.active:
        messages.error(request, "This auction is already closed.")
        return redirect("listing_detail", listing_id=listing.id)

    highest_bid = listing.highest_bid
    if highest_bid:
        listing.winner = highest_bid.bidder

    listing.active = False
    listing.save()

    messages.success(request, "Auction closed successfully.")
    return redirect("listing_detail", listing_id=listing.id)


@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method != "POST":
        return redirect("listing_detail", listing_id=listing.id)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.listing = listing
        comment.commenter = request.user
        comment.save()
        messages.success(request, "Comment added.")
    else:
        messages.error(request, "Comment cannot be empty.")

    return redirect("listing_detail", listing_id=listing.id)


@login_required
def watchlist(request):
    listings = request.user.watchlisted_listings.select_related("owner", "category").all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
    })


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })


def category_listings(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    listings = category.listings.select_related("owner", "category").filter(active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings,
    })
