from django.urls import path
from .views import index, product_detail, create_order, OrderListView, DeleteOrder, cancel_order, order_payment, \
    add_to_cart, add_to_wishlist, cart_products, remove_from_wishlist, add_to_wishlist_index, \
    remove_from_wishlist_index, remove_from_cart, add_to_cart_index, remove_from_cart_index, wishlist_products, \
    remove_from_cart_items, remove_from_wishlist_items

urlpatterns = [
    path('', index, name='index'),
    path('products/<int:product_id>/', product_detail, name='product'),
    path('create-order/', create_order, name='create_order'),
    path('orders/', OrderListView, name='order_list'),
    path('orders/delete/<int:order_id>/', DeleteOrder, name='delete_order'),
    path('orders/cancel/<int:order_id>/', cancel_order, name='cancel_order'),
    path('orders/payment/<int:order_id>/', order_payment, name='payment'),
    path('add_to_wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('add_to_wishlist_index/<int:product_id>/', add_to_wishlist_index, name='add_to_wishlist_index'),
    path('remove_from_wishlist/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('remove_from_wishlist_index/<int:product_id>/', remove_from_wishlist_index, name='remove_from_wishlist_index'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('remove_from_cart_index/<int:product_id>/', remove_from_cart_index, name='remove_from_cart_index'),
    path('remove_from_cart_items/<int:product_id>/', remove_from_cart_items, name='remove_from_cart_items'),
    path('remove_from_wishlist_items/<int:product_id>/', remove_from_wishlist_items, name='remove_from_wishlist_items'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('add_to_cart_index/<int:product_id>/', add_to_cart_index, name='add_to_cart_index'),
    path('cart/', cart_products, name='cart_items'),
    path('wishlist/', wishlist_products, name='wishlist_products'),
]
