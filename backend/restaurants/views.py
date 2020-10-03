from .models import Restaurant, User, Deal, Order, Item
from rest_framework import viewsets, permissions
from .serializers import RestaurantSerializer, UserSerializer, DealSerializer, OrderSerializer, ItemSerializer
from django.shortcuts import get_object_or_404, reverse
from django.http import JsonResponse, HttpResponseRedirect
import json
# import requests

class RestaurantView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DealView(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ItemView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


def dealInfo(request, deal_id):
    deal = get_object_or_404(Deal, id=int(deal_id))
    food_list = []
    for item in deal.items.all():
        d = {}
        d['name'] = item.name
        d['price'] = item.price
        d['image'] = item.img_url
        food_list.append(d)
    return JsonResponse(food_list,safe=False)

def user_order_info(request, user_id):
    user = get_object_or_404(User, id=user_id)
    order_list = []
    for order in user.orders.all():
        d = {}
        d['deal'] = order.deal.title
        d['restaurant'] = order.deal.restaurant.name
        d['price'] = order.deal.new_price
        order_list.append(d)
    return JsonResponse(order_list, safe=False)

def restaurant_info(request, rest_id):
    rest = get_object_or_404(Restaurant, id=rest_id)
    out = {}
    out['name'] = rest.name

def deal_output(request):
    resp = list((DealView.as_view({'get': 'list'})(request)).data)
    resp = list(map(dict, resp))

    for d in resp:
        rest_id = d['restaurant'].split('/')[-2]
        rest = get_object_or_404(Restaurant, id=rest_id)
        items_info = json.loads(dealInfo(request, d['id']).content.decode('utf-8'))

        d['items'] = items_info
        d['restaurant_name'] = rest.name


    # print(l)
    return JsonResponse(resp, safe=False)

def order_output(request):
    resp = list((OrderView.as_view({'get': 'list'})(request)).data)
    resp = list(map(dict, resp))
    # print(dict(UserView.as_view({'get': 'retrieve'})(request,pk=1).data))
    # print(((UserView.as_view({'get': 'list'})(request,1)).data))
    for d in resp:
        # print(d['user'].split('/')[-2])
        try:
            user_id = int(d['user'].split('/')[-2])
            deal_id = int(d['deal'].split('/')[-2])
        except:
            user_id = 1
            deal_id = 1

        user = get_object_or_404(User, id=user_id)
        deal = get_object_or_404(Deal, id=deal_id)
        rest_id = deal.restaurant.id
        rest = get_object_or_404(Restaurant, id=rest_id)

        d['user_id'] = user_id
        d['user_name'] = user.name
        d['deal_id'] = deal.id
        d['deal_name'] = deal.title
        d['restaurant_id'] = rest.id
        d['restaurant_name'] = rest.name

    return JsonResponse(resp, safe=False)
