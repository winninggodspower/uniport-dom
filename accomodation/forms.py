from django import forms
from .models import Book

# import the model here to populate the form

class BookForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = ['checkin_date', 'checkout_date']

