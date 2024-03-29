from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('createlisting', views.createlisting, name = 'create'),
    path('byTeam', views.active_listing_byteam, name='byTeam'),
    path('listing/<int:id>', views.listing, name='listing'),
    path('removewatchList/<int:id>', views.removewatchList, name='removewatchList'),
    path('addwatchList/<int:id>', views.addwatchList, name='addwatchList'),
    path('watchList', views.watchList, name='watchList'),
    path('comment/<int:id>', views.comment, name='comment')
]
