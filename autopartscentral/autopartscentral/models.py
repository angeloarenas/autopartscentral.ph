from django.db import models
from django.contrib.auth.models import User
import datetime
from smart_selects.db_fields import ChainedForeignKey

# TODO Edit __unicode__ here most specially look at VehicleEngine might need to just combine this table with upper level
# TODO Arrange fields into -> primary key, primary names/identifiers, foreign key (many to one), attributes
# TODO Complete __unicode__ for other tables
# TODO Check the use of many to many field

YEAR_CHOICES = [(r, r) for r in range(1990, datetime.date.today().year+1)]
COUNTRY_CHOICES = (('PH', 'Philippines'), )
ORDER_STATUS_CHOICES = (('PL', 'PLACED'), ('CO', 'CONFIRMED'),
                        ('PR', 'PROCESSED'), ('SH', 'SHIPPED'),
                        ('RE', 'RECEIVED'), )

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile')
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    contact_no = models.CharField(max_length=30)
    default_shipping_address = models.OneToOneField('Address', related_name='userprofile')

    def __unicode__(self):
        return u'%i: %s %s' % (self.user.id, self.first_name, self.last_name)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='addresses')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact_no = models.CharField(max_length=30)
    line_1 = models.CharField(max_length=40)
    line_2 = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=30)
    province = models.CharField(max_length=30)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)

    def __unicode__(self):
        return u'%s %s' % (self.line_1, self.line_2)


class CategoryL1(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=35, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='category_images/')

    class Meta:
        verbose_name_plural = "Category Level 1"

    def __unicode__(self):
        return self.name


class CategoryL2(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=35, unique=True)
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
    slug = models.SlugField(max_length=35, unique=True)
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
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=260, unique=True,
                            help_text='Unique value for shop page URL, created from name.')
    part_number = models.CharField(max_length=30)
    sku = models.IntegerField(unique=True)
    # Todo: Cascading dropdown in parts, no changing of super category in categories | NOT A SOLID FIX
    category_l1 = models.ForeignKey(CategoryL1, related_name='parts')
    category_l2 = ChainedForeignKey(CategoryL2, related_name='parts', blank=True, null=True, chained_field="category_l1", chained_model_field="category")
    category_l3 = ChainedForeignKey(CategoryL3, related_name='parts', blank=True, null=True, chained_field="category_l2", chained_model_field="category")
    brand = models.ForeignKey(Brand, related_name='parts', blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)
    availability = models.BooleanField(default=True)
    compatibility = models.ManyToManyField(Vehicle, blank=True)
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


# TODO percentage vs actual
class OrderDiscount(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=30, unique=True)
    value = models.DecimalField(max_digits=12, decimal_places=2)


# TODO percentage vs actual
class PartDiscount(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=30, unique=True)
    part = models.ForeignKey(Part, related_name='part_discounts')
    value = models.DecimalField(max_digits=12, decimal_places=2)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, related_name='orders')
    shipping_address = models.ForeignKey(Address, related_name='orders')
    placed_timestamp = models.DateTimeField(auto_now=True)
    shipped_timestamp = models.DateTimeField(null=True, blank=True)
    customer_instructions = models.TextField(blank=True)
    status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default='PL')
    discount = models.ForeignKey(OrderDiscount, related_name='orders', null=True, blank=True)


class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name='orderdetails')
    part = models.ForeignKey(Part, related_name='orderdetails')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.IntegerField(default=1)
    discount = models.ForeignKey(PartDiscount, related_name='orderdetails', null=True, blank=True)
