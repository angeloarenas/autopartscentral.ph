from django.contrib import admin
import models
import nested_admin

# Follow this http://www.djangobook.com/en/2.0/chapter06.html


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact_no')


class AddressAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact_no', 'line_1', 'line_2', 'city', 'province')


class CategoryL1Admin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')
    prepopulated_fields = {"slug": ("name",)}


class CategoryL2Admin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'image')
    prepopulated_fields = {"slug": ("name",)}


class CategoryL3Admin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'image')
    prepopulated_fields = {"slug": ("name",)}


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', )


class PartImageInline(admin.TabularInline):
    model = models.PartImage
    extra = 1


class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'part_number', 'sku', 'brand', 'price', 'description', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('compatibility',)
    inlines = [PartImageInline]


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
admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.CategoryL1, CategoryL1Admin)
admin.site.register(models.CategoryL2, CategoryL2Admin)
admin.site.register(models.CategoryL3, CategoryL3Admin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Part, PartAdmin)
admin.site.register(models.VehicleMake, VehicleMakeAdmin)
admin.site.register(models.Vehicle, VehicleAdmin)
admin.site.register(models.Order)
admin.site.register(models.OrderDetails)
