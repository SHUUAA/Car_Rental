from decimal import Decimal

from django.conf import settings
from django.db import models

from cars.models import Car, Discount


class Booking(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Booking #{self.pk} — {self.car} ({self.status})'

    @property
    def days(self):
        return (self.end_date - self.start_date).days + 1

    def compute_total(self):
        days = Decimal(self.days)
        base = self.car.daily_rate * days
        if self.discount:
            base = base * (Decimal(100 - self.discount.percentage) / Decimal(100))
        return base.quantize(Decimal('0.01'))


class Payment(models.Model):
    METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('cash', 'Cash on pickup'),
        ('gcash', 'GCash'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE,
                                   related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for booking #{self.booking_id} ({self.method})'


class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE,
                                   related_name='review')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review {self.rating}/5 for booking #{self.booking_id}'
