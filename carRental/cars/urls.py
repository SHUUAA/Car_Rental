from django.urls import path

from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.car_list, name='list'),
    path('<int:pk>/', views.car_detail, name='detail'),
    path('owner/', views.owner_cars, name='owner_cars'),
    path('owner/new/', views.owner_car_new, name='owner_car_new'),
    path('owner/<int:pk>/edit/', views.owner_car_edit, name='owner_car_edit'),
    path('owner/<int:pk>/delete/', views.owner_car_delete, name='owner_car_delete'),
    path('owner/discounts/', views.owner_discounts, name='owner_discounts'),
]
