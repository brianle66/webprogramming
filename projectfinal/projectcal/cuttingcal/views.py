import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.paginator import Paginator
# Create your views here.
def myproject(request):
    
    if request.user.is_authenticated:
        project_list = Project.objects.filter(owner=request.user).order_by('-date')  # Get all projects and order by date

        # Set the number of items per page
        per_page = 10

        paginator = Paginator(project_list, per_page)  # Create Paginator object
        page_number = request.GET.get('page')  # Get the current page number from the request
        projects_per_page = paginator.get_page(page_number)  # Get the current page

        return render(request, 'cuttingcal/myproject.html', {'projects_per_page': projects_per_page})
    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))
    
def project(request, projectcode):

    return render(request, 'cuttingcal/project.html')

def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "cuttingcal/index.html",)

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "cuttingcal/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "cuttingcal/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "cuttingcal/register.html")
    
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
            return render(request, "cuttingcal/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "cuttingcal/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))