from textwrap import indent
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    #path("<str:>", views.entry, name="entry"),
    path("search", views.search, name="search")
]
