from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from cars.models import Car

from .forms import BookingForm, PaymentForm, ReviewForm
from .models import Booking


def _is_customer(user):
    profile = getattr(user, 'profile', None)
    return profile and profile.is_customer


def _is_owner(user):
    profile = getattr(user, 'profile', None)
    return profile and profile.is_owner


def _has_overlap(car, start_date, end_date, exclude_pk=None):
    qs = Booking.objects.filter(
        car=car,
        status__in=[Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED],
    ).filter(
        Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
    )
    if exclude_pk:
        qs = qs.exclude(pk=exclude_pk)
    return qs.exists()


@login_required
def booking_new(request, car_id):
    if not _is_customer(request.user):
        return HttpResponseForbidden('Only customers can book.')
    car = get_object_or_404(Car, pk=car_id, is_available=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            sd = form.cleaned_data['start_date']
            ed = form.cleaned_data['end_date']
            if _has_overlap(car, sd, ed):
                form.add_error(None, 'Those dates overlap an existing booking.')
            else:
                booking = form.save(commit=False)
                booking.customer = request.user
                booking.car = car
                booking.discount = form.cleaned_data.get('discount')
                booking.total_cost = booking.compute_total()
                booking.save()
                messages.success(request, 'Booking created. Please pay to confirm.')
                return redirect('bookings:pay', pk=booking.pk)
    else:
        form = BookingForm()
    return render(request, 'bookings/booking_form.html', {'form': form, 'car': car})


@login_required
def my_bookings(request):
    if not _is_customer(request.user):
        return HttpResponseForbidden('Customers only.')
    today = timezone.now().date()
    qs = Booking.objects.filter(customer=request.user).select_related('car', 'discount')
    for b in qs:
        if b.status == Booking.STATUS_CONFIRMED and b.end_date < today:
            b.status = Booking.STATUS_COMPLETED
            b.save(update_fields=['status'])
    return render(request, 'bookings/my_bookings.html', {'bookings': qs})


@login_required
def pay(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    if booking.status != Booking.STATUS_PENDING:
        messages.info(request, 'This booking is not awaiting payment.')
        return redirect('bookings:my_bookings')
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.amount = booking.total_cost
            payment.save()
            booking.status = Booking.STATUS_CONFIRMED
            booking.save(update_fields=['status'])
            messages.success(request, 'Payment recorded. Booking confirmed.')
            return redirect('bookings:my_bookings')
    else:
        form = PaymentForm()
    return render(request, 'bookings/pay.html', {'form': form, 'booking': booking})


@login_required
def review(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    if booking.status != Booking.STATUS_COMPLETED:
        messages.info(request, 'You can review only after the booking completes.')
        return redirect('bookings:my_bookings')
    if hasattr(booking, 'review'):
        messages.info(request, 'You already reviewed this booking.')
        return redirect('bookings:my_bookings')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.booking = booking
            r.save()
            messages.success(request, 'Thanks for your review!')
            return redirect('bookings:my_bookings')
    else:
        form = ReviewForm()
    return render(request, 'bookings/review.html', {'form': form, 'booking': booking})


@login_required
def owner_bookings(request):
    if not _is_owner(request.user):
        return HttpResponseForbidden('Owners only.')
    qs = Booking.objects.filter(car__owner=request.user).select_related('car', 'customer')
    return render(request, 'bookings/owner_bookings.html', {'bookings': qs})
