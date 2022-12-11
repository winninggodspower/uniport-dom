from django.urls import path, re_path
from . import views

urlpatterns = [
    path('accomodation', views.accomodation.as_view(), name='accomodation'),
    path('checkout_apartment/<int:apartment_id>', views.checkoutApartment.as_view(), name='checkout'),

    re_path('like_apartment', views.like_apartment, name='like_apartment'),
]
