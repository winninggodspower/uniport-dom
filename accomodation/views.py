from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date

from .models import Apartment, Like, Book
from .forms import BookForm

# Create your views here.
class accomodation(View):
    def get(self, request):
        context = {
            'Apartments': Apartment.objects.exclude(booked = True).all(),
        }
        return render(request, 'accomodation.html', context)

@csrf_exempt
def like_apartment(request):
    liked = False
    apartment_id = json.loads(request.body.decode()).get('apartment_id')
    apartment = get_object_or_404(Apartment, pk=apartment_id)

    if request.method == 'POST' and request.user.is_authenticated:
        if not apartment.has_liked(request.user):
            apartment.add_like(request.user)
            liked = True

    return HttpResponse(json.dumps({
        'liked': liked,
        'apartment_like_count': apartment.like_count(),
        'apartment_id': apartment.id,
    }))


class checkoutApartment(View):
    template = 'checkout.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(checkoutApartment, self).dispatch(*args, **kwargs)
    
    def get(self, request, apartment_id):
        apartment = get_object_or_404(Apartment, pk=apartment_id)

        if apartment.booked:
            messages.info(request, 'room already booked')
            return redirect('home')

        context = {
            'apartment': apartment,
            'apartment_images': apartment.get_images(),
        }
        return render(request, self.template, context)

    def post(self, request, apartment_id):
        context = {}
        apartment = get_object_or_404(Apartment, pk=apartment_id)
        body = json.loads(request.body.decode())
        payment_response = body['payment_response']
        
        if apartment.booked:
            context['message'] = 'apartment already booked',
            context['type'] = 'unsuccessful',
            return HttpResponse(json.dumps(context))

        book = Book(
            user= request.user,
            apartment= apartment,
            checkin_date= date.fromisoformat(body['checkin_date']),
            checkout_date= date.fromisoformat(body['checkout_date']),
            amount= body['amount'],
            duration = date.fromisoformat(body['checkout_date']) - date.fromisoformat(body['checkin_date']), 
            reference= payment_response['reference'],
        )

        if book.is_payment_confirmed():
            book.save()
            context['message'] = 'payment successful',
            context['type'] = 'success',

        else:
            context['message'] = 'payment unsuccessful',
            context['type'] = 'unsuccessful',

        return HttpResponse(json.dumps(context))


# @crsf_excempt
def validate_book_detail(request, apartment_id):#
    request_body = json.loads(request.body.decode())
    checkin_date = request_body.get('checkin_date')
    checkout_date = request_body.get('checkout_date')
    apartment = get_object_or_404(Apartment, pk=apartment_id)

    if request.method == 'POST' and request.user.is_authenticated:
        form = BookForm(
            user=request.user,
            apartment=apartment,
            checkin_date=checkin_date,
            checkout_date=checkout_date
        )
        valid = False
        if form.is_valid():
            valid = True

        
        return HttpResponse(json.dumps({
            'valid': valid,
            'message': form.errors,
        }))
