from django.contrib import admin
import models
import nested_admin

# Follow this http://www.djangobook.com/en/2.0/chapter06.html


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact_no')


class CategoryL1Admin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')


class CategoryL2Admin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'image')


class CategoryL3Admin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'image')


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', )


class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'part_number', 'sku', 'brand', 'price', 'description', 'availability')
    filter_horizontal = ('compatibility',)


class VehicleInline(nested_admin.NestedTabularInline):
    model = models.Vehicle
    extra = 0


class VehicleModelInline(nested_admin.NestedStackedInline):
    model = models.VehicleModel
    extra = 0
    inlines = [VehicleInline]


class VehicleMakeAdmin(nested_admin.NestedModelAdmin):
    list_display = ('name', )
    inlines = [VehicleModelInline]


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'make', 'model', 'year_start', 'year_end', 'engine', 'trim')

    def make(self, obj):
        return obj.model.make


admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.CategoryL1, CategoryL1Admin)
admin.site.register(models.CategoryL2, CategoryL2Admin)
admin.site.register(models.CategoryL3, CategoryL3Admin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Part, PartAdmin)
admin.site.register(models.VehicleMake, VehicleMakeAdmin)
admin.site.register(models.Vehicle, VehicleAdmin)
