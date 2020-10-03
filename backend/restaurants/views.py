from .models import Restaurant, User, Deal, Order, Item
from rest_framework import viewsets, permissions
from .serializers import RestaurantSerializer, UserSerializer, DealSerializer, OrderSerializer, ItemSerializer
from django.shortcuts import get_object_or_404, reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from twilio.rest import Client
from django.views.decorators.http import require_POST
import os


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure

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

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def deal_output(request):
    resp = list((DealView.as_view({'get': 'list'})(request._request)).data)
    resp = list(map(dict, resp))

    for d in resp:
        rest_id = d['restaurant'].split('/')[-2]
        rest = get_object_or_404(Restaurant, id=rest_id)
        items_info = json.loads(dealInfo(request, d['id']).content.decode('utf-8'))

        d['items'] = items_info
        d['restaurant_name'] = rest.name


    # print(l)
    return Response(resp)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def order_output(request):
    resp = list((OrderView.as_view({'get': 'list'})(request._request)).data)
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
        d['discount_price'] = deal.new_price
    return Response(resp)


from django.views.decorators.csrf import csrf_exempt


@require_POST
@csrf_exempt
def twilio_sms(request):
    account_sid = os.getenv('ACC_SID')
    auth_token = os.getenv('AUTH_TOKEN')

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    msg = body.get('msg')
    number = body.get('number')
    if (msg == None or number == None):
        return HttpResponse(status=401)

    client = Client(account_sid, auth_token)

    if account_sid == None or auth_token == None:
        return HttpResponse(status=500)

    message = client.messages \
        .create(
        body=msg,
        from_='+18339980513',
        to=number
    )
    print(message.sid)
    return(HttpResponse('SMS {} successful'.format(msg)))

    # print(message.sid)