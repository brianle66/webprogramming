
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('newpost', views.newpost, name='newpost'),
    path('editpost/<int:id>', views.edit_post, name='editpost'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('unfollow', views.unfollow, name='unfollow'),
    path('follow', views.follow, name='follow'),
    path('following', views.following, name='following')
]
