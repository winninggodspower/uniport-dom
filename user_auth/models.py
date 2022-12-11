from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(verbose_name = "email address", max_length=254, unique=True)
    phone = PhoneNumberField()
    def __str__(self):
        return self.username