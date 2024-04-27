from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Post, User, Follow, Like
from django.core.paginator import Paginator
import json
def index(request):
    all_posts = Post.objects.all().order_by('-id')
    paginator = Paginator(all_posts,5)
    page_number = request.GET.get('page')
    posts_per_page = paginator.get_page(page_number)

    #get all the likes
    all_likes = Like.objects.all()

    all_liked_posts = []

    try:
        for like in all_likes:
            if like.user.id == request.user.id:
                all_liked_posts.append(like.post.id)
    except:
        all_liked_posts = []

    return render(request, "network/index.html",{
        'posts_per_page' : posts_per_page,
        'all_liked_posts' : all_liked_posts
    })

def remove_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.filter(user=user, post=post)
    like.delete()
    return JsonResponse({'message': 'Like removed successfully'})

def add_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    new_like = Like(user=user, post=post)
    new_like.save()
    return JsonResponse({'message': 'Like added successfully'})

def following(request):
    current_user = request.user
    following_list = Follow.objects.filter(user=current_user)
    all_posts = Post.objects.all().order_by('-id')

    following_posts = []

    for post in all_posts:
        for person in following_list:
            if person.follower == post.author:
                following_posts.append(post)
    
    paginator = Paginator(following_posts,5)
    page_number = request.GET.get('page')
    posts_per_page = paginator.get_page(page_number)
    return render(request, "network/following.html",{
        'posts_per_page' : posts_per_page
    })


def profile(request, id):
    login_user = request.user
    profile_user = User.objects.get(pk=id)
    all_posts = Post.objects.filter(author=profile_user).order_by('-id')
    paginator = Paginator(all_posts,5)
    page_number = request.GET.get('page')
    posts_per_page = paginator.get_page(page_number)

    following = Follow.objects.filter(user=profile_user)
    followers = Follow.objects.filter(follower=profile_user)

    try:
        checkFollow = followers.filter(user=login_user)
        if len(checkFollow) > 0:
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False

    return render(request, "network/profile.html",{
        'posts_per_page' : posts_per_page,
        'username' : profile_user.username,
        'following' : following,
        'followers' : followers,
        'isfollowing' : isFollowing,
        'profileuser' : profile_user
    })

def follow(request):
    userfollow = request.POST['userfollow']
    current_user = request.user
    follow_user = User.objects.get(username=userfollow)
    f = Follow(user=current_user, follower=follow_user)
    f.save()
    profileid = follow_user.id
    return HttpResponseRedirect(reverse(profile, kwargs={'id' : profileid}))

def unfollow(request):
    userfollow = request.POST['userfollow']
    current_user = request.user
    follow_user = User.objects.get(username=userfollow)
    f = Follow.objects.get(user=current_user, follower=follow_user)
    f.delete()
    profileid = follow_user.id
    return HttpResponseRedirect(reverse(profile, kwargs={'id' : profileid}))

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
