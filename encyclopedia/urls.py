from textwrap import indent
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("search", views.search, name="search"),
    path("edit",views.edit, name="edit")
]
