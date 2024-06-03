import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, get_object_or_404
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
    
def project(request, code):
    '''
    View detail of one project including:
        - Project ID
        - Orders inside the project
        - Order sizes and quantity of each
        - Style of each order
    '''
    project = get_object_or_404(Project, code=code)
    
    if project.owner == request.user:
        orders = project.orders.all()  # Get all orders associated with the project
        
        # Fetch sizes and styles for each order
        order_details = []
        for order in orders:
            sizes = order.sizes.all()  # Get all sizes for the order
            style = order.style  # Get the style of the order
            order_details.append({
                'order': order,
                'sizes': sizes,
                'style': style,
            })
        
        return render(request, 'cuttingcal/project.html', {
            'project': project,
            'order_details': order_details,
        })
    else:
        return render(request, 'cuttingcal/index.html')
    
@csrf_exempt
def update_project(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f'Received data: {data}')
            code = data.get('code')
            name = data.get('name')
            date = data.get('date')
            customer_name = data.get('customer')

            project = get_object_or_404(Project, code=code)

            if project.owner != request.user:
                return JsonResponse({'error': 'Unauthorized access'}, status=403)

            customer, created = Customer.objects.get_or_create(name=customer_name)
            logger.info(f'Customer: {customer}, Created: {created}')

            project.name = name
            project.date = date
            project.customer = customer
            project.save()

            return JsonResponse({'success': True})
        except Exception as e:
            logger.error(f'Error updating project: {e}')
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

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