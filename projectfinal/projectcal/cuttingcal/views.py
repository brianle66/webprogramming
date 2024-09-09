import json
import logging

logger = logging.getLogger(__name__)
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.paginator import Paginator

# Create your views here.

@csrf_exempt
def create_or_update_project(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        project_name = data.get('project_name').strip()
        customer_name = data.get('customer_name').strip()

        customer, created_customer = Customer.objects.get_or_create(
            name__iexact=customer_name,
            defaults={'name': customer_name}
        )

        project, created_project = Project.objects.get_or_create(
            project_name__iexact=project_name,
            customer_name=customer,
            defaults={'project_name': project_name, 'customer_name': customer}
        )

        if not created_project:
            Order.objects.create(project=project, qty=100)  # Example: creating a new order for the project

        response_status = 'created' if created_project else 'updated'
        return JsonResponse({'status': response_status})

def check_customer_name(request):
    customer_name = request.GET.get('name', None).strip().lower()
    data = {
        'available': not Customer.objects.filter(name__iexact=customer_name).exists()
    }
    return JsonResponse(data)

def check_project_name(request):
    project_name = request.GET.get('name', None)
    data = {
        'available': not Project.objects.filter(project_name=project_name).exists()
    }
    return JsonResponse(data)

def calculation(request):
    if request.user.is_authenticated:
        fabrics = Fabric.objects.all()
        styles = Style.objects.all()
        fabric_comp = ['A','B','C','D']
        return render(request, 'cuttingcal/calculation.html',{
            "fabrics" : fabrics,
            "styles" : styles,
            "fabric_comp" : fabric_comp
        })
    else:
        return HttpResponseRedirect(redirect_to= "register")

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

def get_order_detail(request, projectcode, orderid):
    try:
        project = get_object_or_404(Project, code=projectcode)
        logger.info(f"Project found: {project}")
        
        order = get_object_or_404(Order, id=orderid, project=project)
        logger.info(f"Order found: {order}")
        
        order_details = {
            'id': order.id,
            'date': order.date.isoformat(),
            'style': order.style.name,
        }
        return JsonResponse(order_details)
    except Exception as e:
        logger.error(f"Error fetching order details: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    
def update_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order_date = request.POST.get('date')
        order_style = request.POST.get('style')

        order = get_object_or_404(Order, id=order_id)
        order.date = order_date
        order.style = get_object_or_404(Style, name=order_style)
        order.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def update_project(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f'Received data: {data}')
            code = data.get('code')
            name = data.get('name')
            date = data.get('date')
            customer_name = data.get('customer')

            # Check the code value
            logger.info(f'Project code: {code}')
            
            project = get_object_or_404(Project, code=code)
            logger.info(f'Found project: {project}')

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