from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django import forms

from .models import User, Listings, Bids, Comments
import pdb;

'''
Journal:
1. Two types of saving methods on models(database)
1.1 save directly by using xxx.save()
1.2 new_listing = form.save(commit=False)
    new_listing.lister = request.user
    new_listing.save()
    (this method is to add new stuff to the database such as current user before saving)
'''


class CreateListing(ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'start_bid', 'description', 'category', 'picture']

class BidListing(forms.Form):
    place_bid = forms.FloatField(label="place_bid")

class CommentsOnListing(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

def index(request):
    listings = Listings.objects.all()

    return render(request, "auctions/index.html",{
        "listings": listings,
        "delete": False
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

@login_required
def create(request):
    if request.method == "POST":
        #breakpoint()
        form = CreateListing(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.lister = request.user
            new_listing.save()
            return render(request, "auctions/create.html",{
                "form": CreateListing(), 
                "success_create": True
           })
        else:
            return render(request, "auctions/create.html",{
                "form": CreateListing(),
                "unsuccess_create": True
            })

           
    return render(request, "auctions/create.html",{
        "form": CreateListing()
    })
    

def bid_listing(request, list_id):
    #can add to watchlist, and watchlist we can remove
    #bid, must be equal or larger than the starting bid, must be greater if placed bid
    #can close the auction if its the creator
    #
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    list = Listings.objects.get(pk=list_id)
    if request.user in list.watchers.all():
        list.watch = True
        #breakpoint()
    else:
        #breakpoint()
        list.watch = False
    #breakpoint()    
    show_comments = Comments.objects.filter(auction_listing=list)
    #**interesting part
    #Place bid
    if request.method == "POST":
        if 'update_bid' in request.POST:
            form = BidListing(request.POST)
            if form.is_valid():
                #breakpoint()
                #place_bid
                #This is how we use related models (ForeignKey)
                if (form.cleaned_data["place_bid"] >= list.start_bid):
                    if (list.current_bid is not None):
                        if(form.cleaned_data["place_bid"] > list.current_bid):
                            list.current_bid = form.cleaned_data["place_bid"]
                            list.buyer = request.user
                            new_bid = Bids(auction_listing=list, bidder = request.user, offer = form.cleaned_data["place_bid"])
                            new_bid.save()
                            list.save()
                        else:
                            return render(request, "auctions/listing.html",{
                                "list": list,
                                "form": BidListing(), 
                                "error_messages": True,
                                "comment_form":CommentsOnListing(),
                                "comments":show_comments
                            })
                    else:
                        list.current_bid = form.cleaned_data["place_bid"]
                        list.buyer = request.user
                        new_bid = Bids(auction_listing=list, bidder = request.user, offer = form.cleaned_data["place_bid"])
                        new_bid.save()
                        list.save()
                else:
                    return render(request, "auctions/listing.html",{
                        "list": list,
                        "form": BidListing(), 
                        "error_messages": True,
                        "comment_form":CommentsOnListing(),
                        "comments":show_comments
                    })
        elif 'update_comment' in request.POST:
            form = CommentsOnListing(request.POST)
            if form.is_valid():
                new_comment = Comments(content=form.cleaned_data["comment"], user=request.user, auction_listing=list)
                new_comment.save()
            return render(request, "auctions/listing.html",{
                "list": list,
                "form": BidListing(), 
                "error_messages": False,
                "comment_form":CommentsOnListing(),
                "comments":show_comments
            })

        
        return render(request, "auctions/listing.html",{
            "list": list,
            "form": BidListing(), 
            "error_messages": False,
            "comment_form":CommentsOnListing(),
            "comments":show_comments
        })

    return render(request, "auctions/listing.html",{
        "list": list,
        "form": BidListing(),
        "error_messages": False,
        "comment_form":CommentsOnListing(),
        "comments":show_comments
    })

def watchlist(request, list_id):
    #path has to add the parameter as well in order to work
    list = Listings.objects.get(pk=list_id)
    #breakpoint()
    if request.user in list.watchers.all():
        list.watchers.remove(request.user)
        return HttpResponseRedirect(reverse("index"))
    else:
        list.watchers.add(request.user)
        return HttpResponseRedirect(reverse("index"))

def deletelist(request, list_id):
    #SomeModel.objects.filter(id=id).delete() or  instance = SomeModel.objects.get(id=id) -> instance.delete()
    list_to_be_delete = Listings.objects.get(pk=list_id)
    list_to_be_delete.active = False
    list_to_be_delete.save()
    
    return HttpResponseRedirect(reverse("index"))


def userwatchlist(request):
    user_watchlist = Listings.objects.filter(watchers=request.user)
    return render(request, "auctions/userwatchlist.html",{
        "userwatchlists": user_watchlist
    })

def category(request):
    all_list = Listings.objects.all()
    #all_category = all_list.category
    all_category = []
    for list in all_list:
        if list.active == True:
            if list.category not in all_category:
                all_category.append(list.category)
    

    return render(request, "auctions/category.html", {
        "categories": all_category
    })

def find_category(request, entry):
    list_by_category = Listings.objects.filter(category=entry)
    return render(request, "auctions/find.html",{
        "filteredlists" : list_by_category
    })

