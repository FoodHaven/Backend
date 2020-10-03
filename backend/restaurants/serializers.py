from rest_framework import serializers
from django.urls import reverse
from restaurants.models import Restaurant, Deal, User, Order, Item

class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'deals', 'url', 'items')
        read_only_fields = ('deals','items')

class DealSerializer(serializers.HyperlinkedModelSerializer):
    items_info_url = serializers.SerializerMethodField('generate_items_url')
    def generate_items_url(self, deal):
        return reverse('deal_items', args=[deal.id])

    class Meta:
        model = Deal
        fields = ('id', 'title', 'description','original_price','new_price',
                  'items', 'restaurant', 'orders', 'items_info_url',
                  'final_votes', 'url')
        read_only_fields = ('orders',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # orders = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), many=True, write_only=True)
    orders_info_url = serializers.SerializerMethodField('generate_orders_url')
    def generate_orders_url(self, user):
        return reverse('user_orders', args=[user.id])
    class Meta:
        model = User
        fields = ('id', 'name', 'orders', 'phonenumber', 'orders_info_url', 'url')
        read_only_fields = ('orders',)

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'deal', 'created', 'url')

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    # url =
    # items_info_url = serializers.CharField(default="Hi")
    # def generate_items_url(self, :
    class Meta:
        model = Item
        fields = ('id', 'name', 'restaurant', 'price', 'img_url', 'url')
        # read_only_fields = ('restaurant', 'deal')