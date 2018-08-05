from .models import Address
from django import forms


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
