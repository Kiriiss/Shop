from django import forms
from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ivan'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ivanov'}))
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Russian, street, Lenina 1 d.1'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ivan@gmail.com'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')
