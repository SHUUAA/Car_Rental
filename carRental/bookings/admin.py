from django.contrib import admin

from .models import Booking, Payment, Review


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'car', 'start_date', 'end_date',
                    'total_cost', 'status')
    list_filter = ('status',)
    search_fields = ('customer__username', 'car__brand', 'car__model')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'method', 'paid_at')
    list_filter = ('method',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating', 'created_at')
    list_filter = ('rating',)
