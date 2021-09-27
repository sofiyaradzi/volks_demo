from staff.models import UserProfile
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.views import PasswordChangeView
from .forms import StaffRegisterForm, StaffUpdateForm, PasswordChangingForm, StaffPersonalForm

from customer.models import Service
from django.db.models import Count, Q
from datetime import datetime

# Create your views here.

# from django.conf import settings

# User = settings.AUTH_USER_MODEL
from django.contrib.auth import get_user_model
User = get_user_model()


@login_required(redirect_field_name='volks_home')
def staff_home(request):

    # technicians = User.objects.filter(
    #     groups__name='Technician').annotate(all=Count('service')).annotate(
    #         completed=Count('service', filter=Q(
    #             service__status='Completed'))).annotate(
    #         pending=Count('service', filter=Q(service__status='Pending')))

    today = datetime.now().today()

    all = Count('service', filter=Q(service__date__year=today.year) &
                Q(service__date__month=today.month))

    completed = Count('service', filter=Q(
        service__status='Completed') & Q(service__date__year=today.year) &
        Q(service__date__month=today.month))

    pending = Count('service', filter=Q(
        service__status='Pending') & Q(service__date__year=today.year) &
        Q(service__date__month=today.month))

    technicians = User.objects.filter(
        groups__name='Technician').annotate(all=all).annotate(completed=completed).annotate(
        pending=pending)

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            all = Count('service', filter=Q(service__date__gte=start_date) &
                        Q(service__date__lte=end_date))

            completed = Count('service', filter=Q(
                service__status='Completed') & Q(service__date__gte=start_date) &
                Q(service__date__lte=end_date))

            pending = Count('service', filter=Q(
                service__status='Pending') & Q(service__date__gte=start_date) &
                Q(service__date__lte=end_date))

            technicians = User.objects.filter(
                groups__name='Technician').annotate(all=all).annotate(completed=completed).annotate(
                    pending=pending)

            context = {'technicians': technicians,
                       'start_date': start_date, 'end_date': end_date}
            return render(request, 'registration/staff_home.html', context)

        elif start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

            all = Count('service', filter=Q(service__date__gte=start_date))

            completed = Count('service', filter=Q(
                service__status='Completed') & Q(service__date__gte=start_date))

            pending = Count('service', filter=Q(
                service__status='Pending') & Q(service__date__gte=start_date))

            technicians = User.objects.filter(
                groups__name='Technician').annotate(all=all).annotate(completed=completed).annotate(
                    pending=pending)

            context = {'technicians': technicians, 'start_date': start_date}
            return render(request, 'registration/staff_home.html', context)

        elif end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            all = Count('service', filter=Q(service__date__lte=end_date))

            completed = Count('service', filter=Q(
                service__status='Completed') & Q(service__date__lte=end_date))

            pending = Count('service', filter=Q(
                service__status='Pending') & Q(service__date__lte=end_date))

            technicians = User.objects.filter(
                groups__name='Technician').annotate(all=all).annotate(completed=completed).annotate(
                    pending=pending)

            context = {'technicians': technicians, 'end_date': end_date}
            return render(request, 'registration/staff_home.html', context)

    context = {'technicians': technicians, 'today': today}
    return render(request, 'registration/staff_home.html', context)


@ login_required(redirect_field_name='volks_home')
def staff_register(request):
    if request.method == 'POST':
        form = StaffRegisterForm(request.POST)
        if form.is_valid():
            User = form.save()
            group = form.cleaned_data['group']
            group.user_set.add(User)
            return redirect('staff_home')
    else:
        form = StaffRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@ login_required(redirect_field_name='volks_home')
def myprofile(request):
    UserProfile.objects.get_or_create(user=request.user)
    form = StaffUpdateForm(request.POST or None, instance=request.user)
    form2 = StaffPersonalForm(request.POST or None,
                              instance=request.user.userprofile)
    if form.is_valid():
        form.save()
        return redirect('myprofile')
    context = {'form': form, 'form2': form2}
    return render(request, 'registration/myprofile.html', context)


class ChangePassword(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('myprofile')


@ login_required(redirect_field_name='volks_home')
def staff_personal_profile(request):
    form2 = StaffPersonalForm(request.POST or None,
                              instance=request.user.userprofile)
    form = StaffUpdateForm(instance=request.user)

    if form2.is_valid():
        form2.save()
        return redirect('myprofile')

    context = {'form': form, 'form2': form2}
    return render(request, 'registration/myprofile.html', context)
