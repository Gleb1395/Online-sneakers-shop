from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from sneakers_shop.models import Carts, Sneakers


class CartAddForm(forms.ModelForm):
    class Meta:
        model = Carts
        fields = ["sneakers", "count_cart"]

    sneakers = forms.ModelChoiceField(queryset=Sneakers.objects.all(), required=True)
    count_cart = forms.IntegerField(min_value=1, required=True)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "phone_number", "email", "password1", "password2"]
