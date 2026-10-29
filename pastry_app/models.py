from django.db import models

# Create your models here.

class PastryDb(models.Model):

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class OrderDb(models.Model):

    customer_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    pastry_id = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateField()

    status = models.CharField(null=True,blank=True)
    token = models.PositiveIntegerField(null=True,blank=True)
    pickup_time = models.TimeField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return self.customer_name
    








