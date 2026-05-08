from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from cars.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),
    path('cars/', include('cars.urls')),
    path('bookings/', include('bookings.urls')),
]
