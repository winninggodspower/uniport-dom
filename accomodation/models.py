from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import datetime
from django.urls import reverse

from .paystack import Paystack

User = get_user_model()
Max_Aparment_Images = 3

def valid_checkout_date(checkout_date):
    if checkout_date <= datetime.date.today():
        raise ValidationError('checkout date cannot be today or a past date')

def validate_apartment_image_count(apartment_id):
    apartment = Apartment.objects.get(pk = apartment_id)

    if apartment.apartmentimage_set.count() >= Max_Aparment_Images:
        raise ValidationError('This Apartment Image has reached it max number')
    return


# Create your models here.

class Apartment(models.Model):
    title = models.CharField( max_length=50)
    description = models.TextField()
    price = models.PositiveIntegerField()

    thumbnail = models.ImageField( upload_to='ApartmentThumbnails')
    booked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    def add_like(self, user):
        if self.has_liked(user):
            raise ValidationError('user has already liked this apartment')
            return
        like = Like(user=user, apartment=self)
        like.save()

    def like_count(self):
        return self.like_set.count()

    def has_liked(self, user):
        if self.like_set.filter(user = user):
            return True
        False

    def get_images(self) -> list:
        return self.apartmentimage_set.all()


    

        
class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, unique=True)
    
    checkin_date = models.DateField()
    checkout_date = models.DateField(validators=[valid_checkout_date])
    duration = models.DurationField(blank=True, null=True)
    amount = models.IntegerField(default=300)

    reference = models.CharField(max_length=100)
    made_payment = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.checkin_date > self.checkout_date:
            return ValidationError('Checkout date most come after checkin date')

        if not self.is_payment_confirmed() and not self.get_booked_price() == self.amount:
            return ValidationError('Payment was unsuccessful')

        self.made_payment = True
        self.apartment.booked = True
        self.apartment.save()

        return super().save()

    def is_payment_confirmed(self) -> bool:
        res = Paystack().confirm_payment(self.reference)

        if res['status'] == 'success' and res['amount']/100 == self.amount:
            return True
        
        return False

    def get_booked_price(self) -> int:
        return self.apartment.price/30 * self.duration.days

    def __str__(self) -> str:
        return self.apartment.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.apartment.title

class ApartmentImage(models.Model):
    image = models.ImageField( upload_to='ApartmentImage')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, validators=[validate_apartment_image_count])


    def __str__(self) -> str:
        return self.image.url

class ApartmentProperty(models.Model):
    property = models.CharField( max_length=100)
    # icon = FAIconField()
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)

    def __str__(self):
        return self.property
    