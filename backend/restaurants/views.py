from .models import Restaurant, User, Deal, Order, Item
from rest_framework import viewsets, permissions
from .serializers import RestaurantSerializer, UserSerializer, DealSerializer, OrderSerializer, ItemSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


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
