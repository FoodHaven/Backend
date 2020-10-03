from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=15)
    # many to one with Order

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    # many to one with Deal
    # many to one with Item

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, related_name='items', on_delete=models.CASCADE)
    img_url = models.CharField(max_length=1000)
    price = models.FloatField()
    def __str__(self):
        return self.name

class Deal(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='deals', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    original_price = models.FloatField()
    new_price = models.FloatField()
    img_url = models.CharField(max_length=1000)
    items = models.ManyToManyField(Item)

    final_votes = models.IntegerField()

    # Many to one with Order

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, related_name='orders', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{} -> {}".format(self.user.__str__(), self.deal.__str__())


