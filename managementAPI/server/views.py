from django.shortcuts import render
from django.views import View
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .serializers import MenuItemSerializer, UserSerializer
from .models import MenuItem
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
@api_view(['GET', 'POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def menu_items(request):
    if request.method=='GET':
        queryset = MenuItem.objects.all()
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)

        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        paginator = Paginator(queryset, per_page = perpage)

        try:
            queryset = paginator.page(number=page)
        except EmptyPage:
            queryset = []
        data = MenuItemSerializer(queryset, many=True)
        return Response({'data': data.data})


    if request.method=='POST':
        if request.user.groups.filter(name='Manager').exists():
            serialized_item = MenuItemSerializer(data = request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({"message": "Item Created"}, 201)
        else:
            return Response({"message": "You are not authorized"}, 403)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def single_item(request, pk):
    if request.method=='GET':
        queryset = MenuItem.objects.filter(id=pk)
        data = MenuItemSerializer(queryset, many=True)
        return Response({'data': data.data})


    if request.method=='PUT': # Put uses Encoded Form to Update
        if request.user.groups.filter(name='Manager').exists():
            queryset = MenuItem.objects.filter(id=pk)
            serialized_item = MenuItemSerializer(data = request.data)
            serialized_item.is_valid(raise_exception=True)

            queryset.update(title=serialized_item.data['title'])
            queryset.update(price=serialized_item.data['price'])
            queryset.update(category=serialized_item.data['category'])

            return Response({"data": "Successfully Updated"}, 200)
        else:
            return Response({"message": "You are not authorized"}, 403)


    if request.method=='PATCH': # Patch uses Query Params to Update
        if request.user.groups.filter(name='Manager').exists():
            queryset = MenuItem.objects.filter(id=pk)
            t = request.GET.get('title')
            p = request.GET.get('price')
            c = request.GET.get('category')
            if t:
                queryset.update(title=t)
            if p:
                queryset.update(price=p)
            if c:
                queryset.update(category=c)

            data = MenuItemSerializer(queryset, many=True)
            return Response({'PUT data': data.data})
        else:
            return Response({"message": "You are not authorized"}, 403)


    if request.method=='DELETE':
        if request.user.groups.filter(name='Manager').exists():
            item = MenuItem.objects.get(id=pk)
            if item:
                item.delete()
                return Response({"message": "Successfully deleted"}, 200)
            else:
                return Response({"message": "Item does not exist"})
        else:
            return Response({"message": "You are not authorized"}, 403)


@api_view(['GET', 'POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAuthenticated])
def Managers(request):
    if request.user.groups.filter(name='Manager').exists():
        if request.method=='GET':
            queryset = User.objects.filter(groups__name='Manager')
            serialized_item = UserSerializer(queryset, many=True)
            return Response({"data": serialized_item.data}, 200)

        if request.method=='POST':
            serialized_item = UserSerializer(data = request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({"message": "User account created"}, 201)

    else:
        return Response({"message": "You are not authorized"}, 403)


@api_view(['DELETE'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAuthenticated])
def ManagerView(request, mail):
    if request.user.groups.filter(name='Manager').exists():
        if request.method=='DELETE':
            item = User.objects.get(email=mail)
            if item:
                if item.groups.filter(name="Manager").exists():
                    return Response({"message": "Managers cannot delete Managers"}, 400)
                else:
                    item.delete()
                    return Response({"message": "User successfully removed"}, 200)
            else:
                return Response({"message": "User does not exist"}, 404)

    else:
        return Response({"message": "You are not authorized"}, 403)



@api_view(['GET', 'POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAuthenticated])
def DeliveryCrew(request):
    if request.user.groups.filter(name='Manager').exists():
        if request.method=='GET':
            queryset = User.objects.filter(groups__name='Delivery Crew')
            serialized_item = UserSerializer(queryset, many=True)
            return Response({"data": serialized_item.data}, 200)

        if request.method=='POST':
            serialized_item = UserSerializer(data = request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            delivery_group = Group.objects.get(name='Delivery Crew')
            user = User.objects.filter(email=serialized_item.data['email'])
            id = user[0]
            delivery_group.user_set.add(id)
            return Response({"message": "Successfully created Delivery Crew User"}, 201)

    else:
        return Response({"message": "You are not authorized"}, 403)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def DeliveryCrewView(request, pk):
    if request.user.groups.filter(name='Manager').exists():
        if request.method=='DELETE':
            item = User.objects.get(id=pk)
            if item:
                if item.groups.filter(name="Delivery Crew").exists():
                    item.delete()
                    return Response({"message": "Successfully Deleted Crew"}, 200)
                else:
                    return Response({"message": "User is not Delivery Crew"}, 400)
            else:
                return Response({"message": "User not found"}, 404)

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
