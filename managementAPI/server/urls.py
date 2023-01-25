from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItems.as_view())
]