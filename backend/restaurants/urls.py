from django.urls import path, include
from rest_framework import routers
from . import views

router  = routers.DefaultRouter()
router.register('restaurants', views.RestaurantView)
router.register('deals', views.DealView)
router.register('users', views.UserView)
router.register('orders', views.OrderView)
router.register('items', views.ItemView)

urlpatterns = [
    path('', include(router.urls)),
    path('outputs/deals/', views.deal_output, name='deal_output'),
    path('outputs/orders/', views.order_output, name='order_output'),
    path('send_sms/', views.twilio_sms, name='send_sms'),
    path('deals/items_info/<int:deal_id>/', views.dealInfo, name='deal_items'),
    path('users/orders_info/<int:user_id>/', views.user_order_info, name='user_orders'),
]
