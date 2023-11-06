from django.db import models
from django.db.models.functions import datetime
from django.contrib import admin
from django.urls import path, include
from .resources import POSITIONS, cashier

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
]

class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    take_away = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            return (self.time_out - self.time_in).total_seconds()
        else:
            return (datetime.now() - self.time_in).total_seconds()

 class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)

    cap_big = Product.objects.create(name="Монитор", price=9999.0)
    product_2 = Product.objects.create(name="Клавиатура", price=1060.0)
    product_3 = Product.objects.create(name="Витая пара 1 м", price=109.0)

 class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255,choices=POSITIONS,default=cashier)
    labor_contract = models. IntegerField()

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1,db_column='amount')

    def product_sum(self):
        return self.product.price * self.amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()





