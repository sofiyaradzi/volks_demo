from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_home, name='customer_home'),
    path('register', views.customer_register, name='customer_register'),
    path('search', views.customer_search, name='customer_search'),
    path('profile/<customer_id>', views.customer_profile, name='customer_profile'),
    path('update/<customer_id>', views.customer_update, name='customer_update'),
    path('car_register/<customer_id>', views.customer_car_register,
         name='customer_car_register'),
    path('update/<customer_id>/<plate_number>', views.customer_car_update,
         name='customer_car_update'),
    path('delete/<customer_id>/<plate_number>', views.customer_car_delete,
         name='customer_car_delete'),
    path('car_details/<plate_number>',
         views.customer_car_details, name='customer_car_details'),
    path('service/<customer_id>/<plate_number>',
         views.customer_service_book, name='customer_service_book'),
    path('jobcard/<service_id>', views.customer_jobcard, name='customer_jobcard'),
    path('service/<service_id>',
         views.customer_service_update, name='customer_service_update'),
    path('search_service', views.customer_search_service,
         name='customer_search_service'),

]
