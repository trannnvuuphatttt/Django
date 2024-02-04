from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from ckeditor.fields import RichTextField
from .models import User, ShipmentDetails, Menu, MenuDetails, Bill, Dish, Voucher, Account, Confirm, Address, Food, \
    Time, SaleTime, BillDetails
from django.urls import path
from . import dao


class DickForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Dish
        fields = '__all__'


class CulinaryLocationAdminSite(admin.AdminSite):
    site_header = 'Thống Kê Tài Khoản'

    def get_urls(self):
        return [
            path('CulinaryLocation-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/stats.html')


admin_site = CulinaryLocationAdminSite(name='Tài Khoản')
form = DickForm


class UserAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('/static/css/style.css',)
        }


class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'food_id')
    search_fields = ["name", "price"]
    list_filter = ['name', 'price']
    readonly_fields = ['avatar']
    content = RichTextField()
    form = DickForm

    def avatar(self, dish):
        return mark_safe(
            "<img src='/static/{ìg_url}' alt='{arl}' />".format(img_url=dish.avatar.name, arl=dish.subject))



# Register your models here.

admin_site.register(User)
admin_site.register(ShipmentDetails)
admin_site.register(Menu)
admin_site.register(MenuDetails)
admin_site.register(Bill)
admin_site.register(Dish, DishAdmin)
admin_site.register(Voucher)
admin_site.register(Account)
admin_site.register(Confirm)
admin_site.register(Address)
admin_site.register(Food)
admin_site.register(Time)
admin_site.register(SaleTime)
admin_site.register(BillDetails)
