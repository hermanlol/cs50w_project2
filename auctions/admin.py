from django.contrib import admin
from .models import Listings, Bids, Comments
# Register your models here.

class ListingsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "lister", "buyer", "date", "start_bid", "current_bid", "active")

class BidsAdmin(admin.ModelAdmin):
    list_display = ("id", "auction_listing", "bidder", "offer")

class CommentsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "auction_listing", "content")

admin.site.register(Listings, ListingsAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comments, CommentsAdmin)