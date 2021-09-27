from django.contrib import admin
from .models import Customer, Car, Service, ServiceDescription
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export import resources, fields
from django.db import IntegrityError

# Register your models here.


class CarResource(resources.ModelResource):
    customer = fields.Field(
        column_name='customer',
        attribute='customer',
        widget=ForeignKeyWidget(Customer, 'phone_number'))

    class Meta:
        model = Car
        skip_unchanged = True
        report_skipped = True

        import_id_fields = ('plate_number',)
        fields = ('plate_number', 'customer',  'car_model',
                  'chasis_number',)
        exclude = ('id',)

    # def save_instance(self, instance, using_transactions=True, dry_run=False):
    #     try:
    #         super(CarResource, self).save_instance(
    #             instance, using_transactions, dry_run)
    #     except IntegrityError:
    #         pass


class CustomerResource(resources.ModelResource):

    class Meta:
        model = Customer
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('phone_number',)
        fields = ('name', 'phone_number', 'email',)
        exclude = ('id',)


class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('phone_number', 'name', 'email',  'date_registered')
    resource_class = CustomerResource


class CarAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('plate_number', 'customer', 'chasis_number',
                    'car_model', 'date_registered')
    resource_class = CarResource


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'car', 'customer_remarks')


class ServiceDescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'description', 'price')

# @admin.register(Customer)
# class userdata(ImportExportModelAdmin):
#     pass


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceDescription, ServiceDescriptionAdmin)
