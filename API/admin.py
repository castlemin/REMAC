from django.contrib import admin
from .models import CustomUser, Request, Product


class CustomUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CustomUser._meta.fields]


admin.site.register(CustomUser, CustomUserAdmin)


class RequestAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Request._meta.fields]


admin.site.register(Request, RequestAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]


admin.site.register(Product, ProductAdmin)
