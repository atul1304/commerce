from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class Category(models.Model):
    categoryvalue=models.CharField(max_length=20,blank=True)

    def __str__(self):
        return self.categoryvalue

class AuctionListings(models.Model):
    title=models.CharField(max_length=50)
    desc=models.TextField()
    active=models.BooleanField(default=True)
    price=models.FloatField()
    date=models.DateTimeField(auto_now_add=True)
    upload=models.FileField(upload_to="images/",null=True,blank=True)
    category=models.ForeignKey(Category,blank=True,null=True,on_delete=models.CASCADE,related_name="auction_categories")
    createdby=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    def isvalidfirstbid(self,bid):
        return bid>self.price

class Bid(models.Model):
    bid_item=models.ForeignKey(AuctionListings,on_delete=models.CASCADE,related_name="auction_bid")
    bidprice=models.FloatField()
    createdby=models.ForeignKey(User,on_delete=models.CASCADE)


    def isvalid_bid(self,bidprice):
        return bidprice>self.bidprice

class WatchList(models.Model):
    watchList=models.ManyToManyField(AuctionListings,blank=True,related_name="auctionwatchers")
    createdby=models.ForeignKey(User,on_delete=models.CASCADE,related_name="watchers")

    def __str__(self):
        return f"{self.id}"

class Comment(models.Model):
    item=models.ForeignKey(AuctionListings,on_delete=models.CASCADE,related_name="auctioncomments")
    comment=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    createdby=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment