from django.contrib import admin

from .models import Car, Discount


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'car_type', 'daily_rate',
                    'owner', 'is_available')
    list_filter = ('car_type', 'transmission', 'fuel', 'is_available')
    search_fields = ('brand', 'model', 'license_plate')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'percentage', 'owner', 'valid_from', 'valid_until')
    search_fields = ('code',)
