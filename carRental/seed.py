"""Run with: python manage.py shell < seed.py"""
from decimal import Decimal

from django.contrib.auth.models import User

from accounts.models import Profile
from cars.models import Car, Discount


def get_or_create_user(username, role, **extra):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': f'{username}@example.com', **extra},
    )
    if created:
        user.set_password('demo1234')
        user.save()
    profile = user.profile
    profile.role = role
    profile.save()
    return user


owner = get_or_create_user('demo_owner', Profile.ROLE_OWNER,
                           first_name='Demo', last_name='Owner')
customer = get_or_create_user('demo_customer', Profile.ROLE_CUSTOMER,
                              first_name='Demo', last_name='Customer')

samples = [
    dict(brand='Toyota', model='Corolla', year=2022, car_type='sedan',
         transmission='automatic', fuel='petrol', seats=5,
         license_plate='ABC-1234', daily_rate=Decimal('45.00'),
         image='https://images.unsplash.com/photo-1590362891991-f776e747a588?w=900'),
    dict(brand='Honda', model='CR-V', year=2023, car_type='suv',
         transmission='automatic', fuel='hybrid', seats=5,
         license_plate='XYZ-9988', daily_rate=Decimal('72.00'),
         image='https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=900'),
    dict(brand='Tesla', model='Model 3', year=2024, car_type='luxury',
         transmission='automatic', fuel='electric', seats=5,
         license_plate='EV-2024', daily_rate=Decimal('120.00'),
         image='https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=900'),
    dict(brand='Ford', model='Transit', year=2021, car_type='van',
         transmission='manual', fuel='diesel', seats=8,
         license_plate='VAN-555', daily_rate=Decimal('95.00'),
         image='https://images.unsplash.com/photo-1551830820-330a71b99659?w=900'),
    dict(brand='Mazda', model='3', year=2023, car_type='hatchback',
         transmission='manual', fuel='petrol', seats=5,
         license_plate='HB-321', daily_rate=Decimal('50.00'),
         image='https://images.unsplash.com/photo-1502877338535-766e1452684a?w=900'),
    dict(brand='BMW', model='X5', year=2024, car_type='luxury',
         transmission='automatic', fuel='petrol', seats=5,
         license_plate='LUX-001', daily_rate=Decimal('180.00'),
         image='https://images.unsplash.com/photo-1555215695-3004980ad54e?w=900'),
]

for data in samples:
    Car.objects.update_or_create(
        license_plate=data['license_plate'],
        defaults={'owner': owner, **data},
    )

print(f'Owner: demo_owner / demo1234')
print(f'Customer: demo_customer / demo1234')
print(f'Cars seeded: {Car.objects.count()}')
