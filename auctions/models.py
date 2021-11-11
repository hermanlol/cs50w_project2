from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=64)
    active = models.BooleanField(default=True)
    start_bid = models.FloatField()
    current_bid = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(default=django.utils.timezone.now)
    description = models.TextField(null=True, max_length=400)
    category = models.CharField(max_length=32)
    lister = models.ForeignKey(User, on_delete=models.PROTECT, related_name="lister_listing")
    watchers = models.ManyToManyField(User, blank=True, related_name="watch_listing")
    buyer = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    picture = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.id},{self.title} - Start bid : {self.start_bid} - Current bid : {self.current_bid} - Creator : {self.lister}"

class Bids(models.Model):
    auction_listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.FloatField()
    datetime = models.DateTimeField(default=django.utils.timezone.now)

class Comments(models.Model):
    content = models.CharField(max_length=640)
    datetime = models.DateTimeField(default=django.utils.timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(Listings, on_delete=models.CASCADE)