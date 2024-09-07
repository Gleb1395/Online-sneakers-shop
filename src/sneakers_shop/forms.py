from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from sneakers_shop.models import Carts, Sneakers


class CartAddForm(forms.ModelForm):
    class Meta:
        model = Carts
        fields = ["sneakers", "count_cart"]

    sneakers = forms.ModelChoiceField(queryset=Sneakers.objects.all(), required=True)
    count_cart = forms.IntegerField(min_value=1, required=True)


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Second Name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "phone_number", "email", "password1", "password2"]


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "password"}))
