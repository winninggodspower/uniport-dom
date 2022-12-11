from django.contrib import admin
from django import forms
from .models import Like, Apartment, ApartmentImage, ApartmentProperty, Book
from icon_picker_widget.widgets import IconPickerWidget
# Register your models here.
class ApartmentAdmin(admin.ModelAdmin):
    exclude = ('duration',)
    
# class ApartmentPropertyAdminForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(ApartmentPropertyAdminForm, self).__init__(*args, **kwargs)
#         self.fields['icon'].widget = IconPickerWidget()

# class ApartmentPropertyAdmin(admin.ModelAdmin):
#     form = ApartmentPropertyAdminForm


admin.site.register(Like)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(ApartmentImage)
admin.site.register(Book)
admin.site.register(ApartmentProperty)
