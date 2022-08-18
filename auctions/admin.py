from xml.etree.ElementTree import Comment
from django.contrib import admin
from .models import AuctionListings, Bid, Category, User, WatchList, Comment
# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListings)
admin.site.register(Bid)
admin.site.register(WatchList)
admin.site.register(Comment)
admin.site.register(Category)