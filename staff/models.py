from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.deletion import CASCADE
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password, **other_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have a username')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            first_name=str(first_name.title()),
            last_name=last_name,
            username=username,
        )

        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, email, username, first_name, last_name, password, **other_fields):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.save()
        return user

        # other_fields.setdefault('is_staff', True)
        # other_fields.setdefault('is_admin', False)
        # other_fields.setdefault('is_active', True)

        # if other_fields.get('is_staff') is not True:
        #     raise ValueError(
        #         'Staff must be assigned to is_staff=True.')

        # return self.create_user(email, username, first_name, last_name, password, **other_fields)

    def create_superuser(self, email, username, first_name, last_name, password, **other_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
        # other_fields.setdefault('is_staff', True)
        # other_fields.setdefault('is_superuser', True)
        # other_fields.setdefault('is_active', True)

        # if other_fields.get('is_staff') is not True:
        #     raise ValueError(
        #         'Superuser must be assigned to is_staff=True.')
        # if other_fields.get('is_superuser') is not True:
        #     raise ValueError(
        #         'Superuser must be assigned to is_superuser=True.')

        # return self.create_user(email, username, first_name, last_name, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)       # an admin user
    is_superuser = models.BooleanField(default=False)   # a superuser

    objects = UserManager()

    USERNAME_FIELD = 'username'
    # Email & Password are required by default.
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
        # return ("%s %s" % (self.first_name, self.last_name))

    def get_short_name(self):
        return self.first_name

    def get_email(self):
        return self.email

    def __str__(self):
        # return self.username
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()
        return super(User, self).save(*args, **kwargs)

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return self.is_admin
    #     # return True

    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return self.is_admin
    #     # return True

    # @property
    # def is_superuser(self):
    #     return self.is_admin

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     return self.staff

    # @property
    # def is_admin(self):
    #     "Is the user a admin member?"
    #     return self.admin


class UserProfile (models.Model):
    def phone_check(phone_number):
        if phone_number.isdigit() == False:
            raise ValidationError('Only enter numbers')
        if phone_number[0] != '6':
            raise ValidationError('Phone Number must start with "6"')

    def nric_check(nric):
        if nric.isdigit() == False:
            raise ValidationError('Only enter numbers')
    user = models.OneToOneField(User, null=True, on_delete=CASCADE)
    phone_number = models.CharField(unique=True, max_length=15,
                                    validators=[MinLengthValidator(11), phone_check])
    nric = models.CharField(unique=True, max_length=12, validators=[
                            MinLengthValidator(12), nric_check])
    address = models.TextField(blank=True)
    date_joined = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return str(self.user)
