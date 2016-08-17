from django.db import models
from django.contrib.auth.models import User
import datetime

# TODO Edit __unicode__ here most specially look at VehicleEngine might need to just combine this table with upper level
# TODO Arrange fields into -> foreign key (upper level), name, attributes
# TODO Complete __unicode__ for other tables

YEAR_CHOICES = [(r, r) for r in range(1960, datetime.date.today().year+1)]
COUNTRY_CHOICES = []  # For address also add city and state


class Address(models.Model):
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
    default_shipping_address = models.OneToOneField(Address, related_name='userprofile')  # Subject to change

    def __unicode__(self):
        return u'%i: %s %s' % (self.user.id, self.first_name, self.last_name)


class CategoryL1(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='category_images/')

    def __unicode__(self):
        return self.name


class CategoryL2(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(CategoryL1, related_name='categories')
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='category_images/')

    class Meta:
        unique_together = ('category', 'name')

    def __unicode__(self):
        return self.name


class CategoryL3(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(CategoryL2, related_name='categories')
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='category_images/')

    class Meta:
        unique_together = ('category', 'name')

    def __unicode__(self):
        return self.name


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class Part(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    part_number = models.CharField(max_length=30)
    sku = models.IntegerField(unique=True)
    category_l1 = models.ForeignKey(CategoryL1, related_name='parts')
    category_l2 = models.ForeignKey(CategoryL2, related_name='parts', blank=True, null=True)
    category_l3 = models.ForeignKey(CategoryL3, related_name='parts', blank=True, null=True)
    brand = models.ForeignKey(Brand, related_name='parts', blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='part_images/')
    availability = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class VehicleMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class VehicleModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    make = models.ForeignKey(VehicleMake, related_name='vehicle_models')

    class Meta:
        unique_together = ('name', 'make')

    def __unicode__(self):
        return u'%s %s' % (self.name, self.make)


class VehicleYear(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField(choices=YEAR_CHOICES)
    model = models.ForeignKey(VehicleModel, related_name='vehicle_years')

    class Meta:
        unique_together = ('year', 'model')

    def __unicode__(self):
        return u'%s %s' % (str(self.year), self.model)


class VehicleEngine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    year = models.ForeignKey(VehicleYear, related_name='vehicle_engines')

    class Meta:
        unique_together = ('name', 'year')

    def __unicode__(self):
        return self.name


class VehicleTrim(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    engine = models.ForeignKey(VehicleEngine, related_name='vehicle_trims')

    class Meta:
        unique_together = ('name', 'engine')

    def __unicode__(self):
        return self.name


# Explanation of this design:
class PartVehicleCompatibility(models.Model):
    id = models.AutoField(primary_key=True)
    part = models.ForeignKey(Part, related_name='compatibilities')
    make = models.ForeignKey(VehicleMake, related_name='compatibilities', blank=True, null=True)
    model = models.ForeignKey(VehicleModel, related_name='compatibilities', blank=True, null=True)
    year = models.ForeignKey(VehicleYear, related_name='compatibilities', blank=True, null=True)
    engine = models.ForeignKey(VehicleEngine, related_name='compatibilities', blank=True, null=True)
    trim = models.ForeignKey(VehicleTrim, related_name='compatibilities', blank=True, null=True)

    class Meta:
        unique_together = (('part', 'make', 'model', 'year', 'engine', 'trim'), )

    def __unicode__(self):
        return self.part


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

# Customer notes textfield?


class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name='orderdetails')
    part = models.ForeignKey(Part, related_name='orderdetails')
    quantity = models.IntegerField(default=1)
    discount = models.ForeignKey(Discount, related_name='orderdetails')
    net_price = models.DecimalField(max_digits=12, decimal_places=2)

# Part discount and order discount?
