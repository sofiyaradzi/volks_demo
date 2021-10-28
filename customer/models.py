from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum
# from django.contrib.auth.models import User
# from django.conf import settings

# # Create your models here.
# User = settings.AUTH_USER_MODEL

from django.contrib.auth import get_user_model
User = get_user_model()


# class Sample (models.Model):
#     tittle = models.CharField(max_length=254)


class Customer (models.Model):
    def phone_check(phone_number):
        if phone_number.isdigit() == False:
            raise ValidationError('Only enter numbers')
        if phone_number[0] != '6':
            raise ValidationError('Phone Number must start with "6"')

    name = models.CharField(max_length=254)
    phone_number = models.CharField(unique=True, max_length=15,
                                    validators=[MinLengthValidator(11), phone_check])
    email = models.EmailField(max_length=254, blank=True)
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.email = self.email.lower()
        return super(Customer, self).save(*args, **kwargs)


class Car (models.Model):
    # def plate_check(plate_number):
    #     if Car.objects.filter(
    #             plate_number__iexact=plate_number):
    #         raise ValidationError('Plate Number existed')

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plate_number = models.CharField(
        max_length=20,  unique=True)  # validators=[plate_check]
    chasis_number = models.CharField(max_length=30, blank=True)
    car_model = models.CharField(max_length=254, blank=True)
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.plate_number

    def clean(self):
        self.plate_number = self.plate_number.replace(" ", "")
        self.chasis_number = self.chasis_number.replace(" ", "")

    def save(self, *args, **kwargs):
        self.plate_number = self.plate_number.upper()
        self.chasis_number = self.chasis_number .upper()
        self.car_model = self.car_model.title()
        return super(Car, self).save(*args, **kwargs)


class Service (models.Model):
    class Meta:
        ordering = ['-date', '-id']

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    date = models.DateField(
        auto_now=False, auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    service_advisor = models.CharField(max_length=20, blank=True, null=True)
    customer_remarks = models.TextField()
    car_mileage = models.IntegerField(blank=True, null=True)
    technician = models.ForeignKey(User, limit_choices_to={
                                   'groups__name': "Technician"}, on_delete=models.SET_NULL, blank=True, null=True)
    inspection = models.TextField(blank=True)
    job_dateline = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    next_service_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    next_service_remarks = models.CharField(max_length=300, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending')
    replacement_parts = models.TextField(blank=True, null=True)

    def __int__(self):
        return self.id


# class ServiceDescription (models.Model):
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     description = models.CharField(max_length=300)
#     price = models.DecimalField(decimal_places=2, max_digits=6)

#     def __str__(self):
#         return self.description

#     def save(self, *args, **kwargs):
#         self.description = self.description.capitalize()
#         return super(ServiceDescription, self).save(*args, **kwargs)
