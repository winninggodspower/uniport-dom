from django.shortcuts import render, redirect
from django.views import View
from .models import NaijaWifeCard
from django.contrib import messages

# Create your views here.
class NaijaWifeCardView(View):
    form = NaijaWifeCard

    def get(self, request):
        context = {
        }
        return render(request, 'naija-wife-card.html', context)

    def post(self, request):

        naija_wife_card = NaijaWifeCard.objects.create(
            fullname = request.POST.get('fullname'),
            phone = request.POST.get('phone'),
            email = request.POST.get('email'),
            spouse_name = request.POST.get('spouse-name'),
            spouse_contact = request.POST.get('spouse-phone'),
        )

        naija_wife_card.save()
        messages.success(request, 'successfully requested for naija wife card')

        return redirect('naija_wife_card')