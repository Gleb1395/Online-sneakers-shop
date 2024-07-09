from django import forms

from sneakers_shop.models import Carts, Sneakers


class CartAddForm(forms.ModelForm):
    class Meta:
        model = Carts
        fields = ["sneakers", "count_cart"]

    sneakers = forms.ModelChoiceField(queryset=Sneakers.objects.all(), required=True)
    count_cart = forms.IntegerField(min_value=1, required=True)
