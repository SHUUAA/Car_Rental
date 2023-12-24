from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from .models import Customer, CarOwner, Car, Discount


class CarOwnerForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput, label='Input username')
    password = forms.CharField(widget=forms.TextInput, label='Password')
    firstname = forms.CharField(widget=forms.TextInput, label='First Name')
    lastname = forms.CharField(widget=forms.TextInput, label='Last Name')
    phone_num = forms.CharField(widget=forms.TextInput, label='Phone Number')
    email = forms.CharField(widget=forms.TextInput, label='Email')
    city = forms.CharField(widget=forms.TextInput, label='City')
    street = forms.CharField(widget=forms.TextInput, label='Street')
    zipcode = forms.CharField(widget=forms.TextInput, label='Zip Code')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        instance = self.instance

        # Check if the 'uname' key is in the session
        if 'uname' in self.request.session and instance.pk != self.request.session['uname']:
            raise forms.ValidationError("You are not allowed to edit other profiles.")
        return cleaned_data


    def clean_phone_num(self):
        phone_num = self.cleaned_data['phone_num']
        if not phone_num.isdigit():
            raise ValidationError("Phone number should contain only digits.")
        if len(phone_num) != 11:
            raise ValidationError("Phone number should contain exactly 11 digits.")
        return phone_num

    def clean_zipcode(self):
        zipcode = self.cleaned_data['zipcode']
        if not zipcode.isdigit() or len(zipcode) != 4:
            raise ValidationError("Zipcode should be a 4-digit number.")
        return zipcode

    class Meta:
        model = CarOwner
        fields = ['username', 'password', 'firstname', 'lastname', 'phone_num', 'email', 'city', 'street', 'zipcode']


class CarForm(ModelForm):
    Car_ID = forms.CharField(widget=forms.TextInput, label='Car ID')
    license_Plate = forms.CharField(widget=forms.TextInput, label='License Plate')
    car_Brand = forms.CharField(widget=forms.TextInput, label='Car Brand')
    car_Type = forms.CharField(widget=forms.TextInput, label='Car Type')

    def __init__(self, *args, **kwargs):
        carOwner_ID = kwargs.pop('carowner', None)
        super(CarForm, self).__init__(*args, **kwargs)
        if carOwner_ID:
            self.fields['carOwner_ID'].initial = carOwner_ID

    def clean_license_Plate(self):
        license_plate = self.cleaned_data['license_Plate']
        # Check if a car with the same license plate exists in the database
        if Car.objects.filter(license_Plate=license_plate).exists():
            raise ValidationError("This license plate already exists.")
        return license_plate

    class Meta:
        model = Car
        fields = ['Car_ID', 'license_Plate', 'car_Brand', 'car_Type', 'carOwner_ID']
        widgets = {
            'carOwner_ID': forms.HiddenInput
        }


class DiscountForm(ModelForm):
    DiscountID = forms.CharField(widget=forms.TextInput, label='Discount ID')
    discount_code = forms.CharField(widget=forms.TextInput, label='Discount Code')
    discount_percentage = forms.IntegerField(widget=forms.TextInput, label='Discount Percentage')

    def clean_discount_code(self):
        discount_code = self.cleaned_data['discount_code']
        if Discount.objects.filter(discount_code=discount_code).exists():
            raise ValidationError("This discount code already exists.")
        return discount_code

    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data['discount_percentage']
        if not 0 <= discount_percentage <= 100:
            raise ValidationError("Discount percentage must be between 0 and 100.")
        return discount_percentage

    class Meta:
        model = Discount
        fields = ['DiscountID', 'discount_code', 'discount_percentage']


