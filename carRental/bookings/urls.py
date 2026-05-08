from django.urls import path

from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.my_bookings, name='my_bookings'),
    path('new/<int:car_id>/', views.booking_new, name='new'),
    path('<int:pk>/pay/', views.pay, name='pay'),
    path('<int:pk>/review/', views.review, name='review'),
    path('owner/', views.owner_bookings, name='owner_bookings'),
]
