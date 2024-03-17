from django.contrib import admin

# Register your models here.

from .models import Category,Sub_Category,Product,Contact_Us,Order,Brand

admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Product)
admin.site.register(Contact_Us)
admin.site.register(Order)
admin.site.register(Brand)



