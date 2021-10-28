from customer.models import Customer, Car, Service
from django import forms


class RegisterCustomer(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'phone_number', 'email')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
        labels = {
            'name': '',
            'phone_number': '',
            'email': '',
        }


class RegisterCar(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('customer', 'plate_number', 'car_model', 'chasis_number')
        widgets = {
            'customer': forms.HiddenInput(),
            'plate_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Plate Number'}),
            'car_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Car Model'}),
            'chasis_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Chasis Number'}),
        }
        labels = {
            'plate_number': '',
            'car_model': '',
            'chasis_number': '',
        }


class BookService(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('customer', 'car',
                  'service_advisor', 'customer_remarks')
        widgets = {
            'customer': forms.HiddenInput(),
            'car': forms.HiddenInput(),
            'service_advisor': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Service Advisor', 'id': 'service_advisor'}),
            'customer_remarks': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Customer Remarks', 'style': 'height: 150px'}),
        }
        labels = {
            'customer': '',
            'car': '',
            'service_advisor': '',
            'customer_remarks': '',
        }


class UpdateService(forms.ModelForm):

    class Meta:
        model = Service
        fields = ('status', 'customer', 'car', 'service_advisor', 'customer_remarks', 'car_mileage', 'technician',
                  'inspection', 'replacement_parts', 'job_dateline', 'next_service_date', 'next_service_remarks')
        widgets = {
            'customer': forms.HiddenInput(),
            'car': forms.HiddenInput(),
            'service_advisor': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'customer_remarks': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Customer Remarks', 'style': 'height: 150px'}),
            'car_mileage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mileage'}),
            'technician': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Technician'}),
            'inspection': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Inspection', 'style': 'height: 150px'}),
            'job_dateline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'next_service_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'next_service_remarks': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Next Service Remarks'}),
            'replacement_parts': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Replacement Parts', 'style': 'height: 150px'}),
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
        }
        labels = {
            'customer_remarks': 'Customer Remarks',
            'car_mileage': 'Mileage',
            'technician': 'Technician',
            'inspection': 'Inspection',
            'job_dateline': 'Job Dateline',
            'next_service_date': 'Next Service Date',
            'next_service_remarks': 'Next Service Remarks',
            'replacement_parts': 'Replacement Parts',
            'status': 'Status',
        }
