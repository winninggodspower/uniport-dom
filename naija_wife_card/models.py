from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class NaijaWifeCard(models.Model):
    fullname = models.CharField(max_length=50)
    phone = PhoneNumberField()
    email = models.EmailField(max_length=254)
    spouse_name = models.CharField(max_length=50)
    spouse_contact = PhoneNumberField()
