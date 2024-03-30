from django.db import models
from django.contrib.auth.models import AbstractUser
from dashboard.manager import *
import csv
from django.core.exceptions import ValidationError
import pandas as pd



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 


idchoice = [
        ('CUST_ID', 'CUST_ID'),
        ('SEX', 'SEX'),
    ]


class Campaigns(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    campaign_name = models.CharField(default="",max_length=30)
    delivery_date = models.DateTimeField()
    memo = models.CharField(default="",max_length=20)
    target_list = models.FileField(upload_to='target_lists/')
    campaign_id = models.CharField(choices=idchoice, max_length=10, default="CUST_ID")
    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"
    def __str__(self):
        return self.campaign_name
    
    def clean(self):
        if not self.target_list.name.endswith('.csv'):
            raise ValidationError("File must be a .csv file.")
        try:
            decoded_file = self.target_list.read().decode('utf-8')
            csv_reader = csv.DictReader(decoded_file.splitlines())
            if '金額' not in csv_reader.fieldnames:
                raise ValidationError("CSV file must contain a '金額' field.")
            if '日付' not in csv_reader.fieldnames:
                raise ValidationError("CSV file must contain a '日付' field.")
        except Exception as e:
            raise ValidationError(f"Error while validating your uploaded data: {e}")
        

class Orders(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    order_data = models.FileField(upload_to='order_datas/')
    class Meta:
        verbose_name = "Order Data"
        verbose_name_plural = "Orders Data"
    def __str__(self):
        return self.user.email
    
    def clean(self):
        if not self.order_data.name.endswith('.csv'):
            raise ValidationError("File must be a .csv file.")
        try:
            decoded_file = self.order_data.read().decode('utf-8')
            csv_reader = csv.DictReader(decoded_file.splitlines())
            if '金額' not in csv_reader.fieldnames:
                raise ValidationError("CSV file must contain a '金額' field.")
            if '日付' not in csv_reader.fieldnames:
                raise ValidationError("CSV file must contain a '日付' field.")
        except Exception as e:
            raise ValidationError(f"Error while validating your uploaded data: {e}")