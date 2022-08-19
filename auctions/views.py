from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Category, User,AuctionListings



def index(request):

    return render(request, "auctions/index.html",{
        'auctions':AuctionListings.objects.exclude(active=0).all(),
        'title':'Active Listings'
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

@login_required(login_url='login')
def create(request):
    if request.method=="POST":
        title=request.POST['title']
        desc=request.POST['desc']
        price=request.POST['price']
        file=request.FILES['upload'] if len(request.FILES)>0 else None
        category=Category.objects.get(pk=int(request.POST['categoryname']))
        user=request.user
        
        try:
            createlisting=AuctionListings.objects.create(
                title=title,desc=desc,price=float(price),category=category,upload=file,createdby=user
            )
        except IntegrityError:
            return render(request,"auctions/create.html",{
                "message":IntegrityError
            })
        return HttpResponseRedirect(reverse("index"))

    return render(request,"auctions/create.html",{
                    'categories':Category.objects.all().order_by('categoryvalue')
    })

@login_required(login_url='login')
def listings(request,id):
    data=AuctionListings.objects.get(id=id)
    comment=data.auctioncomments.order_by('-date')
    watchList=data.auctionwatchers.filter(createdby=request.user).first()
    message=None

    if request.method=="POST":
        bidprice=float(request.POST['bidprice'])
        message=bid(data,bidprice,request.user)
        
    return render(request,'auctions/listings.html',{
        'listing':data,
        'item':data.auction_bid.first(),
        'watchList':watchList,
        'comments':comment,
        'message':message
    })


def bid(data,bidprice,user):
        item=data.auction_bid.first()
        if item:
            if item.isvalid_bid(bidprice):
                data.auction_bid.update(bidprice=bidprice,createdby=user)
            else:
                return 'Entered Bid Is Less Then Current Bid'
        elif data.isvalidfirstbid(bidprice):
            data.auction_bid.create(bid_item=data,bidprice=bidprice,createdby=user)
            
        else:
            return 'Bid price is less than original price'


def watchList(request,id):
    if request.method=="POST":
        listing=AuctionListings.objects.get(pk=id)
        watch=request.user.watchers.get_or_create()[0] 
        if request.POST['add']=='add':
            watch.watchList.add(listing)
        else:
            watch.watchList.remove(listing)

    return HttpResponseRedirect(reverse("listings",args=(listing.id,)))


def unlist(request,id):
    if request.method=="POST":
        listing=AuctionListings.objects.get(pk=id)
        listing.active=False
        listing.save()

    return HttpResponseRedirect(reverse("listings",args=(listing.id,)))

def postcomment(request,id):
    if request.method=="POST":
        listing=AuctionListings.objects.get(pk=id)
        comment=request.POST['comment']
        listing.auctioncomments.create(item=listing,comment=comment,createdby=request.user)
        
    return HttpResponseRedirect(reverse("listings",args=(listing.id,)))


def get_watchlist(request):
    
    watch=request.user.watchers.first()
    if watch:
        watch=watch.watchList.all()
    return render(request,'auctions/index.html',{
        'auctions':watch,
        'title':'WatchList'
    })

def list_by_categories(request):
    return render(request,'auctions/categories.html',{
        'categories':Category.objects.all().order_by('categoryvalue')
    })

def list_auctions_categories(request,id):
        data=AuctionListings.objects.filter(category=id,active=1)
        return render(request,'auctions/index.html',{
            'auctions':data,
            'title': "Active Listings"
        })


