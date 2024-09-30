from django.contrib import admin
from .models import *
from .models import ProductDetail
from .models import Order

class ProductAdmin(admin.ModelAdmin):
     list_display = ('title','price','description')

# Register your models here.

admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(Booking)
admin.site.register(Order)
# admin.site.register(Offer,OfferAdmin)

