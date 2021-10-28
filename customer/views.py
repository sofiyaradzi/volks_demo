from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import Customer, Car, Service
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
import xlwt
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


@ login_required(redirect_field_name='volks_home')
def customer_service_delete(request, service_id, customer_id):
    service = Service.objects.get(id=service_id)
    if request.method == 'POST':
        service.delete()
        return render(request, 'customer/delete_success.html')
        # return redirect('customer_profile', customer_id)
        # cant redirect to previous page (view service) because the service id is deleted
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {'service': service}
    return render(request, 'customer/customer_service_delete.html', context)


@ login_required(redirect_field_name='volks_home')
def customer_delete(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        customer.delete()
        return render(request, 'customer/delete_success.html')
        # cant redirect to previous page (view service) because the service id is deleted
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {'customer': customer}
    return render(request, 'customer/customer_delete.html', context)


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

    # if the download data button is clicked
    if request.method == 'GET' and 'download' in request.GET:
        # to get the values of selected filter values by user
        if myFilter.data['technician']:
            filtered_tech = str(User.objects.get(
                id=myFilter.data['technician']))
        else:
            filtered_tech = 'All'

        if myFilter.data['status']:
            filtered_status = (myFilter.data['status'])
        else:
            filtered_status = 'All'

        if myFilter.data['date_min']:
            filtered_date_min = myFilter.data['date_min']
            filtered_date_min = datetime.strptime(
                filtered_date_min, '%Y-%m-%d').date()
        else:
            filtered_date_min = 'All'

        if myFilter.data['date_max']:
            filtered_date_max = myFilter.data['date_max']
            filtered_date_max = datetime.strptime(
                filtered_date_max, '%Y-%m-%d').date()
        else:
            filtered_date_max = 'All'

        # custom filename
        filename = "ServiceReport" + "_Technician_" + str(filtered_tech) + "_Status_" + \
            str(filtered_status) + "_From_" + str(filtered_date_min) + "_To_" + \
            str(filtered_date_max) + ".xls"

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'filename="{}"'.format(filename)

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('report', cell_overwrite_ok=True)
        ws.show_grid = False

        # approximately adjusting the col size in mm

        ws.col(0).width = int(10*265)
        ws.col(1).width = int(11*265)
        ws.col(2).width = int(15*265)
        ws.col(3).width = int(25*265)
        ws.col(4).width = int(15*265)
        ws.col(5).width = int(10*265)

        # for report summary
        # font height = 300 is size 15 in excel, size*20=height
        ws.write(0, 0, "SERVICE REPORT SUMMARY",
                 xlwt.easyxf("font: bold on,height 260"))

        ws.write(2, 2, "Status:", xlwt.easyxf("align: horiz right"))
        ws.write(2, 3, filtered_status, xlwt.easyxf("align: horiz left"))

        ws.write(3, 2, "Technician:",
                 xlwt.easyxf("align: horiz right"))
        ws.write(3, 3, filtered_tech, xlwt.easyxf("align: horiz left"))

        ws.write(4, 2, "From date:",
                 xlwt.easyxf("align: horiz right"))
        ws.write(4, 3, filtered_date_min, xlwt.easyxf(
            "align: horiz left", num_format_str="DD/MM/YYYY"))

        ws.write(5, 2, "To date:",
                 xlwt.easyxf("align: horiz right"))
        ws.write(5, 3, filtered_date_max, xlwt.easyxf(
            "align: horiz left", num_format_str="DD/MM/YYYY"))

        ws.write(7, 2, "No. of Services Booked:",
                 xlwt.easyxf("align: horiz right"))
        ws.write(7, 3, service_count, xlwt.easyxf("align: horiz left"))
        ws.write(8, 2, "No. of Services Completed:",
                 xlwt.easyxf("align: horiz right"))
        ws.write(8, 3, completed_count, xlwt.easyxf("align: horiz left"))
        ws.write(9, 2, "No. of Services Pending:",
                 xlwt.easyxf("align: horiz right"))
        ws.write(9, 3, pending_count, xlwt.easyxf("align: horiz left"))

        ws.write(12, 0, "SERVICE REPORT LIST",
                 xlwt.easyxf("font: bold on,height 260"))

        # for report list
        row_num = 14

        columns = ['Service ID', 'Date', 'Plate Number',
                   'Customer', 'Technician', 'Status', ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num,
                     columns[col_num], xlwt.easyxf("font: bold on; border: left thin,right thin,top thin,bottom thin"))

        # to iterate the services from myFilter
        rows = services.values_list('id', 'date', 'car__plate_number',
                                    'customer__name', 'technician__first_name', 'status')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], xlwt.easyxf(
                    "border: left thin,right thin,top thin,bottom thin"))
                if col_num == 0:
                    ws.write(row_num, col_num, row[col_num], xlwt.easyxf(
                        "align: horiz center; border: left thin,right thin,top thin,bottom thin"))
                if col_num == 1:
                    ws.write(row_num, col_num, row[col_num], xlwt.easyxf(
                        "align: horiz left; border: left thin,right thin,top thin,bottom thin", num_format_str="DD/MM/YYYY"))

        wb.save(response)

        return response

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


@ login_required(redirect_field_name='volks_home')
def customer_car_register(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    form = RegisterCar(initial={'customer': customer})
    if request.method == 'POST':
        form = RegisterCar(request.POST)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                return render(request, 'customer/error_new_car.html')
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
