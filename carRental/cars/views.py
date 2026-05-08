from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from .forms import CarForm, DiscountForm
from .models import Car, Discount


def _require_owner(request):
    profile = getattr(request.user, 'profile', None)
    return profile and profile.is_owner


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        featured = Car.objects.filter(is_available=True)[:6]
        return render(request, self.template_name, {'featured': featured})


def car_list(request):
    qs = Car.objects.filter(is_available=True)

    q = request.GET.get('q', '').strip()
    car_type = request.GET.get('type', '')
    max_price = request.GET.get('max_price', '')
    transmission = request.GET.get('transmission', '')

    if q:
        qs = qs.filter(Q(brand__icontains=q) | Q(model__icontains=q))
    if car_type:
        qs = qs.filter(car_type=car_type)
    if transmission:
        qs = qs.filter(transmission=transmission)
    if max_price:
        try:
            qs = qs.filter(daily_rate__lte=float(max_price))
        except ValueError:
            pass

    return render(request, 'cars/list.html', {
        'cars': qs,
        'type_choices': Car.TYPE_CHOICES,
        'transmission_choices': Car.TRANSMISSION_CHOICES,
        'filters': {
            'q': q, 'type': car_type,
            'max_price': max_price, 'transmission': transmission,
        },
    })


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'cars/detail.html', {'car': car})


@login_required
def owner_cars(request):
    if not _require_owner(request):
        return HttpResponseForbidden('Owner access only.')
    cars = Car.objects.filter(owner=request.user)
    return render(request, 'cars/owner_list.html', {'cars': cars})


@login_required
def owner_car_new(request):
    if not _require_owner(request):
        return HttpResponseForbidden('Owner access only.')
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            messages.success(request, 'Car listed.')
            return redirect('cars:owner_cars')
    else:
        form = CarForm()
    return render(request, 'cars/owner_form.html', {'form': form, 'mode': 'new'})


@login_required
def owner_car_edit(request, pk):
    if not _require_owner(request):
        return HttpResponseForbidden('Owner access only.')
    car = get_object_or_404(Car, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car updated.')
            return redirect('cars:owner_cars')
    else:
        form = CarForm(instance=car)
    return render(request, 'cars/owner_form.html', {'form': form, 'mode': 'edit', 'car': car})


@login_required
def owner_car_delete(request, pk):
    if not _require_owner(request):
        return HttpResponseForbidden('Owner access only.')
    car = get_object_or_404(Car, pk=pk, owner=request.user)
    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Car removed.')
        return redirect('cars:owner_cars')
    return render(request, 'cars/owner_confirm_delete.html', {'car': car})


@login_required
def owner_discounts(request):
    if not _require_owner(request):
        return HttpResponseForbidden('Owner access only.')
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            d = form.save(commit=False)
            d.owner = request.user
            d.save()
            messages.success(request, 'Discount created.')
            return redirect('cars:owner_discounts')
    else:
        form = DiscountForm()
    discounts = Discount.objects.filter(owner=request.user)
    return render(request, 'cars/owner_discounts.html', {'form': form, 'discounts': discounts})
