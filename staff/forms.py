from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User, Group
from django import forms
# from .models import User
from django.contrib.auth import get_user_model, password_validation
from staff.models import UserProfile

User = get_user_model()


class StaffRegisterForm (UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    first_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'group',
                  'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(StaffRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class StaffUpdateForm (UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    first_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.HiddenInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(StaffUpdateForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'


class PasswordChangingForm (PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password'}),
        label='New Password'
    )
    new_password2 = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password'}),
        label='Confirm Password',
        help_text=password_validation.password_validators_help_text_html()
    )

    class Meta:
        model = User
        # fields = ('old_password', 'new_password1', 'new_password2')


class StaffPersonalForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number',
                  'nric', 'address', 'date_joined')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'nric': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IC Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'style': 'height: 150px'}),
            'date_joined': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'phone_number': 'Phone Number',
            'nric': 'IC Number',
            'address': 'Address',
            'date_joined': 'Date Joined',
        }
