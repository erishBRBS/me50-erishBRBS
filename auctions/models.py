from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Listing(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_listings"
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="listings"
    )
    watchlist = models.ManyToManyField(
        User,
        blank=True,
        related_name="watchlisted_listings"
    )
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="won_listings"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def highest_bid(self):
        return self.bids.order_by("-amount", "-created_at").first()

    @property
    def current_price(self):
        highest = self.highest_bid
        return highest.amount if highest else self.starting_bid

    def __str__(self):
        return self.title


class Bid(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bids"
    )
    bidder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bids"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-amount", "-created_at"]

    def __str__(self):
        return f"{self.bidder.username}: ${self.amount} on {self.listing.title}"


class Comment(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    commenter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.commenter.username} on {self.listing.title}"
