from . import views
from django.urls import path


app_name = 'cars'

urlpatterns =[
    path('', views.HomeView.as_view(), name="index"),
    path('login', views.LoginView.as_view(), name='login'),
    path('logoff', views.LogOff.as_view(), name='logoff'),
    path('CarOwner', views.CarOwnerIndex.as_view(), name='CarOwner'),
    path('displayCar', views.DisplayCar.as_view(), name='displayCar'),
    path('displayDiscount', views.DisplayDiscount.as_view(), name='displayDiscount'),
    path('registerCarOwner', views.RegisterCarOwner.as_view(), name='registerCarOwner'),
    path('editProfileCarOwner', views.EditProfileCarOwner.as_view(), name='editProfileCarOwner'),
    path('AddCar', views.AddCar.as_view(), name='AddCar'),
    path('AddDiscount', views.AddDiscount.as_view(), name='AddDiscount')
]