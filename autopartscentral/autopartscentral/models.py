from django.db import models
from django.contrib.auth.models import User
import datetime

# TODO Edit __unicode__ here most specially look at VehicleEngine might need to just combine this table with upper level
# TODO Arrange fields into -> primary key, primary names/identifiers, foreign key (many to one), attributes
# TODO Complete __unicode__ for other tables
# TODO Check the use of many to many field

YEAR_CHOICES = [(r, r) for r in range(1990, datetime.date.today().year+1)]
COUNTRY_CHOICES = []  # For address also add city and state


class Address(models.Model):  # TODO Not in normal form - city, state, country
    id = models.AutoField(primary_key=True)
    line_1 = models.CharField(max_length=40)
    line_2 = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)  # Just put choices here of states in PH
    country = models.CharField(max_length=20)  # Should be just PH

    def __unicode__(self):
        return u'%s %s' % (self.line_1, self.line_2)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile')
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    contact_no = models.CharField(max_length=13)
    default_shipping_address = models.OneToOneField(Address, related_name='userprofile')

    def __unicode__(self):
        return u'%i: %s %s' % (self.user.id, self.first_name, self.last_name)


class CategoryL1(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='category_images/')

    class Meta:
        verbose_name_plural = "Category Level 1"

    def __unicode__(self):
        return self.name


class CategoryL2(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    category = models.ForeignKey(CategoryL1, related_name='categories')
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='category_images/')

    class Meta:
        unique_together = ('name', 'category')
        verbose_name_plural = "Category Level 2"

    def __unicode__(self):
        return self.name


class CategoryL3(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    category = models.ForeignKey(CategoryL2, related_name='categories')
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='category_images/')

    class Meta:
        unique_together = ('name', 'category')
        verbose_name_plural = "Category Level 3"

    def __unicode__(self):
        return self.name


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class VehicleMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Vehicle Makes"

    def __unicode__(self):
        return self.name


class VehicleModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    make = models.ForeignKey(VehicleMake, related_name='vehicle_models')

    class Meta:
        unique_together = ('name', 'make')
        verbose_name_plural = "Vehicle Models"

    def __unicode__(self):
        return self.name


#PARTIALLY DENORMALIZED TABLE
class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.ForeignKey(VehicleModel, related_name='vehicles')
    year_start = models.IntegerField(choices=YEAR_CHOICES)
    year_end = models.IntegerField(choices=YEAR_CHOICES)
    engine = models.CharField(max_length=50)
    trim = models.CharField(max_length=50)

    class Meta:
        unique_together = ('model', 'year_start', 'year_end', 'engine', 'trim')

    def __unicode__(self):
        return u'%s %s %s %s %s' % (self.model, str(self.year_start), str(self.year_end), self.engine, self.trim)


class Part(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    part_number = models.CharField(max_length=30)
    sku = models.IntegerField(unique=True)
    # Todo: All categories above the set category should be null - solution to the update foreign key problem
    category_l1 = models.ForeignKey(CategoryL1, related_name='parts')  # if category_l3 is set, l1 and l2 should be null
    category_l2 = models.ForeignKey(CategoryL2, related_name='parts', blank=True, null=True)  # if l2 is set l1
    category_l3 = models.ForeignKey(CategoryL3, related_name='parts', blank=True, null=True)  # should be null
    brand = models.ForeignKey(Brand, related_name='parts', blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)
    availability = models.BooleanField(default=True)
    compatibility = models.ManyToManyField(Vehicle)
    created_on = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.name


class PartImage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='part_images/')
    part = models.ForeignKey(Part, related_name='images')


class PartFeatured(models.Model):
    id = models.AutoField(primary_key=True)
    part = models.OneToOneField(Part, related_name='+')


class Discount(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    value = models.DecimalField(max_digits=12, decimal_places=2)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(UserProfile, related_name='orders')
    shipping_address = models.ForeignKey(Address, related_name='orders')
    placed_timestamp = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)


class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name='orderdetails')
    part = models.ForeignKey(Part, related_name='orderdetails')
    quantity = models.IntegerField(default=1)
    discount = models.ForeignKey(Discount, related_name='orderdetails')
    net_price = models.DecimalField(max_digits=12, decimal_places=2)
# Part discount and order discount?
