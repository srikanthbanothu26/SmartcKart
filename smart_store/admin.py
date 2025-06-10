from django.contrib import admin
from .models import Product, Order, Cart, Payments, wishlist


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sales_price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'status')


class CartAdmin(admin.ModelAdmin):
    list_display = ('product',)  #


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('order',)


class wishlistAdmin(admin.ModelAdmin):
    list_display = ('product',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Payments, PaymentsAdmin)
admin.site.register(wishlist, wishlistAdmin)
