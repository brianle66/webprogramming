from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('myproject/', views.myproject, name='myproject'),
    path('project/<str:code>/', views.project, name='project'),
    path('project/<str:projectcode>/<int:orderid>/', views.get_order_detail, name="get_order_detail"),
    path('update_project/', views.update_project, name='update_project'),
    path('update_order/<int:order_id>/', views.update_order, name='update_order'),
    path('calculation', views.calculation, name='calculation'),
    path('check_project_name/', views.check_project_name, name='check_project_name'),
    path('check_customer_name/', views.check_customer_name, name='check_customer_name'),
    path('create_or_update_project/', views.create_or_update_project, name='create_or_update_project'),
    path('check_style_fabric_comp/', views.check_style_fabric_comp, name='check_style_fabric_comp'),
    path('get_order_id/', views.get_order_id, name='get_order_id'),
    path('get_style_img/', views.get_style_img, name='get_style_img'),
]