from django.shortcuts import render
from django.views import View
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

# Create your views here.
@api_view(['GET', 'POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def menu_items(request):
    if request.method=='GET':
        return Response({"message": "Everyone should be able to view this"})

    if request.method=='POST':
        if request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Only Manager Should See This"}, 201)
        else:
            return Response({"message": "You are not authorized"}, 403)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def MenuItemsViewSet(request):
    if request.method=='GET':
        return Response({"message": "Menu Item here"})
    if request.method=='PUT':
        if request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Only Manager Should Put"}, 200)
        else:
            return Response({"message": "You are not authorized"}, 403)
    if request.method=='PATCH':
        if request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Only Manager Should Patch"}, 200)
        else:
            return Response({"message": "You are not authorized"}, 403)
    if request.method=='DELETE':
        if request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Only Manager Should Delete"}, 200)
        else:
            return Response({"message": "You are not authorized"}, 403)


@api_view(['GET', 'POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAuthenticated])
def Managers(request):
    if request.user.groups.filter(name='Manager').exists():
        if request.method=='GET':
            return Response({"message": "Get method in Manager"}, 200)

        if request.method=='POST':
            return Response({"message": "Post method in Manager"}, 201)

    else:
        return Response({"message": "You are not authorized"}, 403)

@api_view(['DELETE'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAuthenticated])
def ManagerView(request):
    if request.user.groups.filter(name='Manager').exists():
        if request.method=='DELETE':
            # add logic to find. If found, return 200. If not found, return 404
            return Response({"message": "Successfully Deleted"}, 200)

    else:
        return Response({"message": "You are not authorized"}, 403)



@api_view(['GET', 'POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAuthenticated])
def DeliveryCrew(request):
    if request.user.groups.filter(name='Manager').exists():
        if request.method=='GET':
            return Response({"message": "Returns all delivery crew"}, 200)

        if request.method=='POST':
            return Response({"message": "Assigns a user to the delivery crew group"}, 201)

    else:
        return Response({"message": "You are not authorized"}, 403)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def DeliveryCrewView(request):
    if request.user.groups.filter(name='Manager').exists():
        if request.method=='DELETE':
            # add logic to find. If found, return 200. If not found, return 404
            return Response({"message": "Successfully Deleted Crew"}, 200)

    else:
        return Response({"message": "You are not authorized"}, 403)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def Cart(request):
    if request.method=='GET':
        return Response({"message": "returns current items in cart"}, 200)

    if request.method=='POST':
        return Response({"message": "Adds current item into cart"}, 201)

    if request.method=='DELETE':
        return Response({"message": "Deletes all menu items"}, 200)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def Orders(request):
    if request.method=='GET':
        if request.user.groups.filter(name='Manager').exists():
            return Response({"message": "orders of all users"}, 200)

        if request.user.groups.filter(name="Delivery Crew").exists():
            return Response({"message": "Orders assigned to Delivery"}, 200)

        return Response({"message": "Order items created by the user"}, 200)

    if request.method=='POST':
        return Response({"message": "Creates a new order item for the user"}, 201)



@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def OrderItems(request):
    if request.method=='GET':
        return Response({"message": "returns all items for order id"}, 200)

    if request.method=='PUT':
        if request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Replace (put) the status of an order"}, 200)

    if request.method=='PATCH':
        if request.user.groups.filter(name='Delivery Crew').exists() or request.user.groups.filter(name='Delivery Crew').exists():
            return Response({"message": "Patches (patch)order status"}, 200)

    if request.method=='DELETE':
        if request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Deletes the order"}, 200)
