from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
# Register your models here.


class UserAdminConfig(UserAdmin):
    model = User
    list_display = ('id', 'email', 'username', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'is_superuser')

    fieldsets = (
        ('Basic Information', {
         'fields': ('email', 'username', 'first_name', 'last_name', 'password', 'groups')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'date_joined')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(User, UserAdminConfig)
