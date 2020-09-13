from django.db import models
from django.utils.timezone import timezone

# Create your models here.

class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    contact = models.IntegerField()
    email_id  = models.EmailField()
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    password = models.CharField(max_length=300)


    def __str__(self):
        return self.name


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    contact = models.IntegerField()
    email_id = models.EmailField()
    addresses = models.CharField(max_length=200)
    password = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Sweets(models.Model):
    sweet_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    sweet_image = models.ImageField(upload_to='media/')
    price = models.IntegerField()

    def __str__(self):
        return self.title


class AddToCart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    sweet_id = models.ForeignKey(Sweets,on_delete=models.CASCADE)
    orders = models.BooleanField(default=False)
    qty = models.IntegerField(default=1)


    def __str__(self):
        return self.sweet_id.title


    def total_price(self):
        return self.qty * self.sweet_id.price


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact = models.IntegerField()
    email = models.EmailField(default=0)
    pin_code = models.IntegerField()
    place = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    land_mark = models.CharField(max_length=200)
    alternative_no = models.IntegerField(default=0)



class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    items = models.ManyToManyField(AddToCart)
    ordered = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add = True)
    order_time = models.DateTimeField(null=True)
    user_address = models.ForeignKey(Address,on_delete=models.SET_NULL,blank=True,null=True)


    def get_total_price(self):
        total = 0
        for x in self.items.all():
            total += x.total_price()
        return total


class Payment(models.Model):
    user = models.ForeignKey(Users,on_delete=models.SET_NULL,blank=True,null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    order_id = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.user.name




















