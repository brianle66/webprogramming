from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name= 'entry'),
    path("search/", views.search, name= 'search'),
    path("newpage/", views.create_new_page, name='new_page'),
    path("editentry/", views.edit_entry, name='edit_entry'),
    path("savededit/", views.save_edit, name='save_edit'),
    path("random/", views.random_entry, name="random_entry")
]
