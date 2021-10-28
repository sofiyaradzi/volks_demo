from django.urls import path
from .views import ChangePassword
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('register/', UserRegisterView.as_view(), name='register'),
    path('', views.staff_home, name='staff_home'),
    path('register/', views.staff_register, name='register'),
    # path('profile/', views.staff_profile, name='staff_profile'),
    # path('password/', auth_views.PasswordChangeView.as_view()),
    path('password/', ChangePassword.as_view(
        template_name='registration/change-password.html'), name='change_password'),
    path('personal_profile/', views.staff_personal_profile,
         name='staff_personal_profile'),
]
