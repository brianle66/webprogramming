from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Team(models.Model):
    teamName = models.CharField(max_length = 64)
    teamCode = models.CharField(max_length = 3)
    def __str__(self) -> str:
        return f'{self.teamName}'
    
class Listing(models.Model):
    title = models.CharField(max_length = 64)
    owner = models.ForeignKey(User, on_delete = models.CASCADE,blank = True, null = True, related_name = 'cars')
    price = models.FloatField()
    team = models.ForeignKey(Team, on_delete = models.CASCADE,blank = True, null = True, related_name = 'cars')
    imgURL = models.CharField(max_length = 1000)
    isActive = models.BooleanField(default = True)
    watchList = models.ManyToManyField(User, blank=True, null=True, related_name='userwatchlist')

    def __str__(self) -> str:
        return f'Name: {self.title}'

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE,blank = True, null = True, related_name = 'authorComment')
    comment = models.CharField(max_length = 300)
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE,blank = True, null = True, related_name = 'listingComment')
    
    def __str__(self) -> str:
        return f'{self.author} comment on {self.listing}'
