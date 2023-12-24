from django.contrib import admin
from .models import CarOwner, Customer, Car, Discount, Booking, Payment

admin.site.register(CarOwner)
admin.site.register(Customer)
admin.site.register(Car)
admin.site.register(Discount)
admin.site.register(Booking)
admin.site.register(Payment)
# Register your models here.
