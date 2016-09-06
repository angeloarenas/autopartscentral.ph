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


class VehicleTrimInline(nested_admin.NestedStackedInline):
    model = models.VehicleTrim
    extra = 0


class VehicleEngineInline(nested_admin.NestedStackedInline):
    model = models.VehicleEngine
    extra = 0
    inlines = [VehicleTrimInline]


class VehicleYearInline(nested_admin.NestedStackedInline):
    model = models.VehicleYear
    extra = 0
    inlines = [VehicleEngineInline]


class VehicleModelInline(nested_admin.NestedStackedInline):
    model = models.VehicleModel
    extra = 0
    inlines = [VehicleYearInline]


class VehicleMakeAdmin(nested_admin.NestedModelAdmin):
    list_display = ('name', )
    inlines = [VehicleModelInline]


class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'make')


class VehicleYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'make', 'model')

    def make(self, obj):
        return obj.model.make


class VehicleEngineAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', '_model', 'year')

    def make(self, obj):
        return obj.year.model.make

    def _model(self, obj):
        return obj.year.model


class VehicleTrimAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', '_model', 'year', 'engine')

    def make(self, obj):
        return obj.engine.year.model.make

    def _model(self, obj):
        return obj.engine.year.model

    def year(self, obj):
        return obj.engine.year

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
#admin.site.register(models.PartVehicleCompatibility)
