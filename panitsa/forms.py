#forms.py
from django import forms
from django.contrib.auth.forms import *
from django.core.exceptions import *
from django.utils.translation import gettext_lazy as _
from django.utils.translation import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        

class RepresentativeForm(forms.ModelForm):
    class Meta:
        model = Representative
        fields = ['image', 'first_name', 'last_name', 'position', 'phone_number']

class Activity_newsForm(forms.ModelForm):
    class Meta:
        model = Activity_news
        fields = ['text', 'date', 'time', 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
class VillagepublicForm(forms.ModelForm):
    class Meta:
        model = Villagepublic
        fields = ['image', 'first_name', 'last_name', 'position', 'phone_number']



class Income_expensesForm(forms.ModelForm):
    class Meta:
        model = Income_expenses
        fields = ['date', 'time', 'income', 'income_amount', 'expenses', 'expenses_amount', 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'income_amount': forms.NumberInput(attrs={'step': '0.01'}),
            'expenses_amount': forms.NumberInput(attrs={'step': '0.01'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = [ 'message', 'image']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'placeholder': 'พิมพ์ข้อความตอบกลับที่นี่...'}),
            
        }


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = [
            'payment_method', 'date', 'subject', 'name', 'address', 
            'phone', 'amount', 'amount_text', 'transfer_receipt'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'payment_method': forms.RadioSelect(choices=Donation.PAYMENT_METHOD_CHOICES),
        }