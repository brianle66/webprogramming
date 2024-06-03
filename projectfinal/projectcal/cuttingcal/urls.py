from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('myproject/', views.myproject, name='myproject'),
    path('project/<str:code>/', views.project, name='project'),
    path('update_project/', views.update_project, name='update_project')
]