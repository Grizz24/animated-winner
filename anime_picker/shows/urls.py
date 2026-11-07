from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_show, name="add_show"),
    path("quick-add/", views.quick_add, name="quick_add"),
    path("pick/", views.pick, name="pick"),
]
