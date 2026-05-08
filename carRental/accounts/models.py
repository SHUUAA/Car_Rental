from django.conf import settings
from django.db import models


class Profile(models.Model):
    ROLE_CUSTOMER = 'customer'
    ROLE_OWNER = 'owner'
    ROLE_CHOICES = [
        (ROLE_CUSTOMER, 'Customer'),
        (ROLE_OWNER, 'Car Owner'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f'{self.user.username} ({self.role})'

    @property
    def is_owner(self):
        return self.role == self.ROLE_OWNER

    @property
    def is_customer(self):
        return self.role == self.ROLE_CUSTOMER
