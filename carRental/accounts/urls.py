from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.CRLoginView.as_view(), name='login'),
    path('logout/', views.CRLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
