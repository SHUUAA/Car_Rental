from django.db import models

# Create your models here.


class CarOwner(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=20)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=11)
    email = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    zipcode = models.IntegerField(default=1)

    def delete(self, *args, **kwargs):
        # Delete associated cars
        Car.objects.filter(carOwner_ID=self).delete()

        # Call the original delete method to delete the car owner
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.username





class Car(models.Model):
    Car_ID = models.IntegerField(default=1, primary_key=True)
    license_Plate = models.CharField(max_length=10)
    car_Brand = models.CharField(max_length=50)
    car_Type = models.CharField(max_length=50)
    carOwner_ID = models.ForeignKey(CarOwner, on_delete=models.CASCADE)


class Discount(models.Model):
    DiscountID = models.IntegerField(default=1, primary_key=True)
    discount_code = models.IntegerField(default=1)
    discount_percentage = models.IntegerField(default=1)

















class Customer(models.Model):
    CustomerID= models.CharField(max_length=50, primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    zipcode = models.IntegerField(default=1)
class Booking(models.Model):
    Booking_ID = models.CharField(max_length=10, primary_key=True)
    username = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car_ID = models.ForeignKey(Car, on_delete=models.CASCADE)
    discount_ID = models.ForeignKey(Discount, on_delete=models.CASCADE)
    booking_StartDate = models.DateField()
    booking_EndDate = models.DateField()
    total_Cost = models.IntegerField(default=1)


class Payment(models.Model):
    PaymentID = models.IntegerField(default=1, primary_key=True)
    username = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_amount = models.IntegerField(default=1)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)
