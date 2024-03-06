from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Team, Listing


def index(request):
    active_listing = Listing.objects.filter(isActive = True)
    allTeam = Team.objects.all()
    return render(request, "auctions/index.html",{
        'active_listing': active_listing,
        'team' : allTeam
    })

def active_listing_byteam(request):
    if request.method == 'POST':
        searchTeam = request.POST['teamName']
        team = Team.objects.get(teamName = searchTeam)
        active_listing = Listing.objects.filter(isActive = True, team = team)
        allTeam = Team.objects.all()
        return render(request, "auctions/index.html",{
            'active_listing': active_listing,
            'team' : allTeam
    })

def createlisting(request):
    if request.method == 'GET':
        allTeam = Team.objects.all()
        return render(request, 'auctions/create.html', {
            'team':allTeam
        })
    else:
        title = request.POST['title']
        price = request.POST['price']
        imgURL = request.POST['imgURL']
        currentUser = request.user
        team = Team.objects.get(teamName = request.POST['team'])
        new_listing = Listing(
            title = title,
            owner = currentUser,
            price = price,
            imgURL = imgURL,
            team = team
        )
        new_listing.save()
        return HttpResponseRedirect(reverse(index))


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
