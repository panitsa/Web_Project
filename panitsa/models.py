#models.py
from django.db import models
from django.contrib.auth.models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import *


User = get_user_model()


class Representative(models.Model):
    image = models.ImageField(upload_to='Representative_images/')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'representative'
        
class Activity_news(models.Model):
    image = models.ImageField(upload_to='images/')
    text = models.TextField()
    time = models.TimeField()
    date = models.DateField()
    
    class Meta:
        db_table = 'activity_news'
        
class Villagepublic(models.Model):
    image = models.ImageField(upload_to='Villagepublic_images/')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)

    class Meta:
        db_table = 'villagepublic'
        
class Income_expenses(models.Model):
    date = models.DateField()
    time = models.TimeField()
    income = models.TextField()
    income_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    expenses = models.TextField()
    expenses_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='Income_expenses_images/')
        
    class Meta:
        db_table = 'income_expenses'

class ChatMessage(models.Model):
    CATEGORY_CHOICES = [
        ('road', 'เรื่องถนน'),
        ('water', 'เรื่องน้ำ'),
        ('electricity', 'เรื่องไฟฟ้า'),
        ('general', 'เรื่องทั่วไป'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admin_message = models.BooleanField(default=False)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)                           
    class Meta:
        db_table = 'chat_message'



class Donation(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('transfer', 'เงินโอน'),
    ]

    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    date = models.DateField()
    subject = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_text = models.CharField(max_length=255)
    transfer_receipt = models.ImageField(upload_to='receipts/', null=True, blank=True)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    class Meta:
        db_table = 'Donation'

