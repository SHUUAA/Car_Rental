from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect

from .models import CarOwner, Car, Discount
from .forms import CarOwnerForm, CarForm, DiscountForm
# Create your views here.


class HomeView(View):
    template = "indexCarOwner.html"

    def get(self, request):

        return render(request, self.template)


class CarOwnerIndex(View):
    template = "indexCarOwner.html"

    def get(self, request):
        return render(request, self.template)


class LoginView(View):
    template = "login.html"

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        error = ""
        uname = request.POST['txtUsername']
        pwd = request.POST['txtPassword']

        account = CarOwner.objects.get(pk=uname)

        if not account:
            error = "Username not existing."
            return render(request, self.template, {'error': error})
        elif pwd != account.password:
            error = "Incorrect password."
            return render(request, self.template, {'error':error})
        else:
            request.session['uname'] = account.username
            return HttpResponseRedirect('/cars/CarOwner')


class LogOff(View):
    def get(self, request):
        if 'uname' in request.session:
            del request.session['uname']
        return HttpResponseRedirect('/cars/login')


class RegisterCarOwner(View):
    template = "registerCarOwner.html"

    def get(self, request):
        form = CarOwnerForm()
        return render(request, self.template, {'form':form})

    def post(self,request):
        form = CarOwnerForm(request.POST, request=request)
        if form.is_valid():
            form.save()
        else:
            return render(request, self.template, {'form': form})
        return HttpResponseRedirect('/cars/login')


class DisplayCar(View):
    template = "DisplayCar.html"

    def get(self, request):
        cars = Car.objects.all()
        return render(request, self.template, {'cars': cars})


class DisplayDiscount(View):
    template = "DisplayDiscount.html"

    def get(self, request):
        cars = Discount.objects.all()
        return render(request, self.template, {'cars': cars})


class EditProfileCarOwner(View):
    template = 'editProfileCarOwner.html'

    def get(self, request):
        carowner = CarOwner.objects.get(pk=request.session['uname'])
        form = CarOwnerForm(instance=carowner, request=request)  # Pass the request object to the form
        return render(request, self.template, {'form': form})

    def post(self, request):
        carowner = CarOwner.objects.get(pk=request.session['uname'])
        form = CarOwnerForm(request.POST, instance=carowner, request=request)  # Pass the request object to the form
        if 'btnUpdate' in request.POST:
            # Update logic remains the same
            if form.is_valid():
                form.save()
            return render(request, self.template, {'form': form})

        elif 'btnDelete' in request.POST:
            # Delete the car owner and redirect to login
            carowner.delete()
            del request.session['uname']
            return redirect('cars:login')

        return render(request, self.template, {'form': form})



class AddCar(View):
    template = "AddCar.html"

    def get(self, request):
        carowner = CarOwner.objects.get(pk=request.session['uname'])
        form = CarForm(carowner=carowner)
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, self.template, {'form': form})


class AddDiscount(View):
    template = "AddDiscount.html"

    def get(self, request):
        form = DiscountForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = DiscountForm(request.POST)
        if form.is_valid():
            discount = form.save(commit=False)
            # Here, associate the Discount with the current CarOwner
            discount.car_owner = CarOwner.objects.get(pk=request.session['uname'])
            discount.save()
            return redirect('cars:AddDiscount')
        return render(request, self.template, {'form': form})
