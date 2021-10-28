import django_filters
from django_filters import DateFilter, CharFilter, DateFromToRangeFilter, DateRangeFilter
from django_filters.widgets import RangeWidget
from .models import Service
from datetime import datetime
from django.utils import timezone
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()


class ServiceFilter(django_filters.FilterSet):

    date = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(
            attrs={'type': 'date', 'class': ' form-control w-25'}),
        label='Date range:',
    )

    status = django_filters.ChoiceFilter(
        choices=Service.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control w-25'})

    )

    technician = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(groups__name='Technician'),
        widget=forms.Select(attrs={'class': 'form-control w-25'})

    )

    class Meta:
        model = Service
        fields = ['status', 'technician']

    # @property
    # def qs(self):
    #     parent = super().qs
    #     if not self.is_valid():
    #         # add default daterange for today
    #         start_date = datetime.now().today()
    #         end_date = datetime.now().today()
    #         field_name = "date"
    #         lookup_gte = "%s__gte" % (field_name)
    #         lookup_lte = "%s__lte" % (field_name)
    #         kwargs = {lookup_gte: start_date, lookup_lte: end_date}
    #         return parent.filter(**kwargs)
    #     else:
    #         return parent

    def __init__(self, *args, **kwargs):
        super(ServiceFilter, self).__init__(*args, **kwargs)
        # at sturtup user doen't push Submit button, and QueryDict (in data) is empty
        if self.data == {}:
            self.queryset = self.queryset.none()
