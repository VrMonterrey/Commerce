from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    active = Listing.objects.filter(isActive=True)
    cat = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings" : active,
        "categories" : cat
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


def addListing(request):
    if request.method == "GET":
        all = Category.objects.all()
        return render(request,"auctions/add.html",{
            "categories" : all
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageUrl = request.POST["imageUrl"]
        price = request.POST["price"]
        category = request.POST["category"]
        user = request.user
        cat = Category.objects.get(name=category)
        bid = Bid(float(price), user = user)
        bid.save()
        new = Listing(
            title=title,
            description=description,
            imageUrl=imageUrl,
            price=bid,
            category=cat,
            owner=user
        )
        new.save()
        return HttpResponseRedirect(reverse(index))

def showCat(request):
    if request.method == "POST":
        submittedCat = request.POST['category']
        category = Category.objects.get(name=submittedCat)
        active = Listing.objects.filter(isActive=True, category=category)
        cat = Category.objects.all()
        return render(request, "auctions/index.html",{
            "listings" : active,
            "categories" : cat,
        })
    
def listing(request, id):
    info = Listing.objects.get(pk=id)
    inWatchList = request.user in info.watchList.all()
    comments = Comment.objects.filter(listing=info)
    isOwner = request.user.username == info.owner.username
    return render(request, "auctions/listing.html",{
        "listing" : info,
        "inWatchlist" : inWatchList,
        "comments" : comments,
        "isOwner" : isOwner
    })

def remove(request, id):
    info = Listing.objects.get(pk=id)
    user = request.user
    info.watchList.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def append(request, id):
    info = Listing.objects.get(pk=id)
    user = request.user
    info.watchList.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def showWatchlist(request):
    user = request.user
    listings = user.ListingOwner.all()
    return render(request, "auctions/watchlist.html",{
        "listings" : listings
    }) 

def postComment(request, id):
    user = request.user
    info = Listing.objects.get(pk=id)
    comment = request.POST["Comment"]
    newComment = Comment(
        author=user,
        listing = info,
        message = comment
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def addBid(request, id):
    new = request.POST['bid']
    info = Listing.objects.get(pk=id)
    inWatchList = request.user in info.watchList.all()
    comments = Comment.objects.filter(listing=info)
    isOwner = request.user.username == info.owner.username
    if not new:
        return render(request, "auctions/listing.html",{
            "listing" : info,
            "check" : False,
            "inWatchlist" : inWatchList,
            "comments" : comments,
            "isOwner" : isOwner
        })
    elif float(new) > float(info.price.bid):
        update = Bid(user=request.user, bid=float(new))
        update.save()
        info.price = update
        info.save()
        return render(request, "auctions/listing.html",{
            "listing" : info,
            "message" : "Bid was updated successfully",
            "update" : True,
            "inWatchlist" : inWatchList,
            "comments" : comments,
            "check" : True,
            "isOwner" : isOwner
        })
    else:
        return render(request, "auctions/listing.html",{
            "listing" : info,
            "message" : "Update failed",
            "update" : False,
            "inWatchlist" : inWatchList,
            "comments" : comments,
            "check" : True,
            "isOwner" : isOwner
        })

def close(request, id):
    info = Listing.objects.get(pk=id)
    info.isActive = False
    info.save()
    inWatchList = request.user in info.watchList.all()
    comments = Comment.objects.filter(listing=info)
    isOwner = request.user.username == info.owner.username
    return render(request, "auctions/listing.html",{
            "message" : "Listing was successfully closed",
            "listing" : info,
            "update" : False,
            "inWatchlist" : inWatchList,
            "comments" : comments,
            "check" : False,
            "isOwner" : isOwner
        })