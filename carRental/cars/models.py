from django.conf import settings
from django.db import models


class Car(models.Model):
    TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
        ('van', 'Van'),
        ('luxury', 'Luxury'),
    ]
    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cars',
    )
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    car_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    fuel = models.CharField(max_length=20, choices=FUEL_CHOICES)
    seats = models.PositiveSmallIntegerField(default=5)
    license_plate = models.CharField(max_length=15, unique=True)
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.URLField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.year} {self.brand} {self.model}'

    @property
    def display_name(self):
        return f'{self.brand} {self.model}'


class Discount(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='discounts',
    )
    code = models.CharField(max_length=20, unique=True)
    percentage = models.PositiveSmallIntegerField()
    valid_from = models.DateField()
    valid_until = models.DateField()

    def __str__(self):
        return f'{self.code} ({self.percentage}%)'
