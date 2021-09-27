from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import Customer, Car, Service, ServiceDescription
from .forms import *
from django.db.models import Count, Q
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from .filters import ServiceFilter
from datetime import datetime
# Create your views here.


@login_required(redirect_field_name='volks_home')
def customer_home(request):

    services = Service.objects.all()
    service_count = Service.objects.all().count()

    completed_count = Service.objects.filter(
        status='Completed').count()

    pending_count = Service.objects.filter(
        status='Pending').count()

    myFilter = ServiceFilter(request.GET, queryset=services)

    services = myFilter.qs
    service_count = myFilter.qs.count()
    completed_count = myFilter.qs.filter(
        status='Completed').count()
    pending_count = myFilter.qs.filter(
        status='Pending').count()

    context = {'services': services, 'service_count': service_count,
               'completed_count': completed_count, 'pending_count': pending_count, 'myFilter': myFilter}
    return render(request, 'customer/customer_home.html', context)


@login_required(redirect_field_name='volks_home')
def customer_register(request):
    if request.method == 'POST':
        form = RegisterCustomer(request.POST)

        if form.is_valid():
            form.save()
            customer = Customer.objects.latest('id')
            context = {'form': form, 'customer': customer}
            return render(request, 'customer/customer_register.html', context)
        else:
            context = {'form': form}
            return render(request, 'customer/customer_register.html', context)

    else:
        form = RegisterCustomer()

        context = {'form': form}
        return render(request, 'customer/customer_register.html', context)


@login_required(redirect_field_name='volks_home')
def customer_search(request):
    if request.method == 'POST':
        searched = request.POST['searched']

        phone_number = Customer.objects.filter(
            phone_number__icontains=searched)
        plate_number = Customer.objects.filter(
            car__plate_number__icontains=searched)
        customers = chain(phone_number, plate_number)

        # Customer.objects.filter(phone_number__icontains=searched) | Customer.objects.filter(car__plate_number__icontains=searched)

        # Customer.objects.filter(Q(phone_number__icontains=searched) | Q(car__plate_number__icontains=searched)

        # Customer.objects.filter(car__plate_number__icontains=searched)
        # Customer.objects.filter(phone_number__icontains=searched)

        context = {'searched': searched, 'customers': customers}
        return render(request, 'customer/customer_search.html', context)

    else:
        return render(request, 'customer/customer_search.html', {})


@login_required(redirect_field_name='volks_home')
def customer_search_service(request):
    if request.method == 'POST':
        searched_service = request.POST['searched_service']

        services = Service.objects.filter(
            id__icontains=searched_service)

        context = {'searched_service': searched_service, 'services': services}
        return render(request, 'customer/customer_search_service.html', context)

    else:
        return render(request, 'customer/customer_search_service.html', {})


@login_required(redirect_field_name='volks_home')
def customer_profile(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    context = {'customer': customer}
    return render(request, 'customer/customer_profile.html', context)


@login_required(redirect_field_name='volks_home')
def customer_update(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    form = RegisterCustomer(request.POST or None, instance=customer)
    if form.is_valid():
        form.save()
        return redirect('customer_profile', customer_id)
    context = {'form': form}
    return render(request, 'customer/customer_update.html', context)


@login_required(redirect_field_name='volks_home')
def customer_car_register(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    form = RegisterCar(initial={'customer': customer})
    if request.method == 'POST':
        form = RegisterCar(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_profile', customer_id)

    # else:
    context = {'form': form, 'customer': customer}
    return render(request, 'customer/customer_car_register.html', context)


@login_required(redirect_field_name='volks_home')
def customer_car_update(request, customer_id, plate_number):
    car = Car.objects.get(plate_number=plate_number)
    form = RegisterCar(request.POST or None, instance=car)
    if form.is_valid():
        form.save()
        return redirect('customer_profile', customer_id)
    context = {'form': form}
    return render(request, 'customer/customer_car_update.html', context)


@login_required(redirect_field_name='volks_home')
def customer_car_delete(request, customer_id, plate_number):
    car = Car.objects.get(plate_number=plate_number)
    if request.method == 'POST':
        car.delete()
        return redirect('customer_profile', customer_id)
    context = {'car': car}
    return render(request, 'customer/customer_car_delete.html', context)


@login_required(redirect_field_name='volks_home')
def customer_car_details(request, plate_number):
    car = Car.objects.get(plate_number=plate_number)
    context = {'car': car}
    return render(request, 'customer/customer_car_details.html', context)


@login_required(redirect_field_name='volks_home')
def customer_service_book(request, customer_id, plate_number):
    customer = Customer.objects.get(pk=customer_id)
    car = Car.objects.get(plate_number=plate_number)
    form = BookService(initial={'car': car, 'customer': customer})
    if request.method == 'POST':
        form = BookService(request.POST)
        if form.is_valid():
            form.save()
            service = Service.objects.latest('id')
            context = {'form': form, 'service': service,
                       'car': car, 'customer': customer}
            return render(request, 'customer/customer_service_book.html', context)
        else:
            context = {'form': form}
            return render(request, 'customer/customer_service_book.html', context)

    else:
        form = BookService(initial={'car': car, 'customer': customer})
        context = {'form': form, 'car': car, 'customer': customer}
        return render(request, 'customer/customer_service_book.html', context)


@login_required(redirect_field_name='volks_home')
def customer_service_update(request, service_id):
    service = Service.objects.get(id=service_id)
    form = UpdateService(request.POST or None, instance=service)
    if form.is_valid():
        form.save()
        messages.success(request, 'Service Updated')
        return redirect('customer_service_update', service_id)
    context = {'form': form, 'service': service}

    return render(request, 'customer/customer_service_update.html', context)


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


@login_required(redirect_field_name='volks_home')
def customer_jobcard(request, service_id):
    filename = "jobcard_service_id_" + str(service_id) + ".pdf"

    service = Service.objects.get(id=service_id)
    template_path = 'customer/jobcard.html'
    context = {'service': service}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="{}"'.format(filename)
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
