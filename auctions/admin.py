from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Bid, Category, Comment, Listing, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "category", "current_price", "active", "winner", "created_at")
    list_filter = ("active", "category", "created_at")
    search_fields = ("title", "description", "owner__username")
    filter_horizontal = ("watchlist",)


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "bidder", "amount", "created_at")
    list_filter = ("created_at",)
    search_fields = ("listing__title", "bidder__username")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "commenter", "created_at")
    list_filter = ("created_at",)
    search_fields = ("listing__title", "commenter__username", "content")
