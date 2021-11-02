from django.contrib import admin
from .models import Listings, Bids, Comments
# Register your models here.

class ListingsAdmin(admin.ModelAdmin):
    list_display = ("id","title")

class BidsAdmin(admin.ModelAdmin):
    list_display = ("id","auction_listing")

class CommentsAdmin(admin.ModelAdmin):
    list_display = ("id","content")

admin.site.register(Listings, ListingsAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comments, CommentsAdmin)