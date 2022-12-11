from django.urls import path, re_path
from . import views

urlpatterns = [
    path('naija_wife_card', views.NaijaWifeCardView.as_view(), name='naija_wife_card'),
]
