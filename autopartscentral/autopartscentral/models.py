from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    line_1 = models.CharField(max_length=40)
    line_2 = models.CharField(max_length=40)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20) #Just put choices here of states in PH
    country = models.CharField(max_length=20) #Should be just PH


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile')
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact_no = models.CharField(max_length=13)
    default_shipping_address = models.OneToOneField(Address, related_name='userprofile') #Subject to change


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    image = models.ImageField(null=True,blank=True,upload_to='category_images/')


class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, related_name='subcategories')
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    image = models.ImageField(null=True,blank=True,upload_to='subcategory_images/')


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    product_number = models.BigIntegerField()
    category = models.ForeignKey(Category, related_name='products')
    subcategory = models.ForeignKey(Subcategory, related_name='products', null=True)
    brand = models.ForeignKey(Brand, related_name='products')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(null=True)
    image = models.ImageField(null=True,blank=True,upload_to='product_images/')
    availability = models.BooleanField(default=True)


class ProductFeatured(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.OneToOneField(Product, related_name='+')


class Discount(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    value = models.DecimalField(max_digits=12, decimal_places=2)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(UserProfile, related_name='orders')
    shipping_address = models.ForeignKey(Address, related_name='orders')
    placed_timestamp = models.DateTimeField(auto_now=True)

#Customer notes textfield?


class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name='orderdetails')
    product = models.ForeignKey(Product, related_name='orderdetails')
    quantity = models.IntegerField(default=1)
    discount = models.ForeignKey(Discount, related_name='orderdetails')
    net_price = models.DecimalField(max_digits=12, decimal_places=2)

#Product discount and order discount?
