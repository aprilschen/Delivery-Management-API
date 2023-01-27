from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items', views.menu_items),
    path('menu-items/<int:pk>', views.single_item),

    path('groups/managers/users', views.Managers),
    path('groups/managers/users/<int:id>', views.ManagerView),

    path('groups/delivery-crew/users', views.DeliveryCrew),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewView),

    path('cart/menu-items', views.Cart),

    path('orders', views.Orders),
    path('orders/<int:pk>', views.OrderItems),

    path('api-token-auth', obtain_auth_token)
]