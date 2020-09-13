from django import forms
from .models import *


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = '__all__'


class SweetForm(forms.ModelForm):
    class Meta:
        model = Sweets
        fields = '__all__'


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('user',)