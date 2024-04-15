from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Post, User
import json

def index(request):
    user = request.user
    all_posts = user.posts.all().order_by('-id')
    return render(request, "network/index.html",{
        'allposts' : all_posts
    })


def edit_post(request, id):
    current_post = Post.objects.get(pk=id)
    if request.method == 'GET':
        return render(request, 'network/editpost.html', {
            'post': current_post
        })
    elif request.method == 'POST':
        current_post.content = request.POST['newcontent']
        current_post.save()
        return HttpResponseRedirect(reverse('index'))


def newpost(request):
    if request.method == 'POST':
        content = request.POST['content']
        author = request.user
        post = Post(content=content, author = author)
        post.save()

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
