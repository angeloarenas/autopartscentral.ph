from django.contrib import admin
import models

# Follow this http://www.djangobook.com/en/2.0/chapter06.html
# TODO Arrange list_display here which ones should go first


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact_no')


class CategoryL1Admin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')


class CategoryL2Admin(admin.ModelAdmin):
    list_display = ('category', 'name', 'description', 'image')


class CategoryL3Admin(admin.ModelAdmin):
    list_display = ('category', 'name', 'description', 'image')


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', )


class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'part_number', 'sku', 'brand', 'price', 'description', 'availability')


class VehicleMakeAdmin(admin.ModelAdmin):
    list_display = ('name', )


class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ('make', 'name')


class VehicleYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'model')


class VehicleEngineAdmin(admin.ModelAdmin):
    list_display = ('year', 'name')


class VehicleTrimAdmin(admin.ModelAdmin):
    list_display = ('engine', 'name')

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.CategoryL1, CategoryL1Admin)
admin.site.register(models.CategoryL2, CategoryL2Admin)
admin.site.register(models.CategoryL3, CategoryL3Admin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Part, PartAdmin)
admin.site.register(models.VehicleMake, VehicleMakeAdmin)
admin.site.register(models.VehicleModel, VehicleModelAdmin)
admin.site.register(models.VehicleYear, VehicleYearAdmin)
admin.site.register(models.VehicleEngine, VehicleEngineAdmin)
admin.site.register(models.VehicleTrim, VehicleTrimAdmin)
