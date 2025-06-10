from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Product, Order, Payments, Cart, wishlist
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
import pytz
from datetime import datetime
from django.utils.timezone import make_aware
from django.contrib.auth.decorators import login_required


def index(request):
    query = request.GET.get('q', '')
    user = request.user

    if query:
        product_list = Product.objects.filter(
            Q(name__icontains=query) | Q(display_name__icontains=query)
        ).order_by('id')
    else:
        product_list = Product.objects.all().order_by('id')

    # Fetch user's cart and wishlist product IDs
    cart_ids = set(Cart.objects.filter(user_id=user.id).values_list('product_id', flat=True))
    wishlist_ids = set(wishlist.objects.filter(user_id=user.id).values_list('product_id', flat=True))

    # Annotate each product with `in_cart` and `in_wishlist`
    for product in product_list:
        product.in_cart = product.id in cart_ids
        product.in_wishlist = product.id in wishlist_ids

    paginator = Paginator(product_list, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {
        'page_obj': page_obj,
        'query': query,
    })


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    in_cart = Cart.objects.filter(product=product, user_id=user.id).exists()
    in_wishlist = wishlist.objects.filter(product=product, user_id=user.id).exists()

    return render(request, 'product.html', {
        'product': product,
        'in_cart': in_cart,
        'in_wishlist': in_wishlist,
    })


@login_required
@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)
            amount = data.get('Amount')
            india_tz = pytz.timezone("Asia/Kolkata")
            local_time = timezone.now().astimezone(india_tz)
            order_date = local_time

            product = Product.objects.get(id=product_id)
            Order.objects.create(product=product, qty=quantity, payment=amount, order_date=order_date,
                                 order_status='confirmed', status=True, user_id=request.user)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def OrderListView(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    user = request.user
    orders = Order.objects.filter(user_id=user.id)

    if start_date and end_date:
        try:
            start = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            end = make_aware(datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59))
            orders = orders.filter(order_date__range=(start, end), user_id=user.id)
        except ValueError:
            pass  # silently ignore invalid dates

    # Sort in descending order so latest orders appear first
    orders = orders.order_by('-id')

    return render(request, 'orders.html', {'ordered_items': orders})


@login_required
def DeleteOrder(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect(reverse('order_list'))


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.order_status = 'cancelled'
    order.save()
    return redirect(reverse('order_list'))


@login_required
def order_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')
        india_tz = pytz.timezone("Asia/Kolkata")
        local_time = timezone.now().astimezone(india_tz)
        payment_date = local_time
        Payments.objects.create(order=order, payment_type=payment_type, payment_status=True, payment_date=payment_date,
                                user_id=request.user)
        order.payment_status = True
        order.save()
        return redirect(reverse('order_list'))

    return render(request, 'payment.html', {'order': order})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not Cart.objects.filter(product=product, user_id=request.user.id).exists():
        Cart.objects.create(product=product, user_id=request.user)
        return redirect(reverse('product', kwargs={'product_id': product_id}))
    return redirect(reverse('product', kwargs={'product_id': product_id}))


@login_required
def add_to_cart_index(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not Cart.objects.filter(product=product, user_id=request.user.id).exists():
        Cart.objects.create(product=product, user_id=request.user)
        return redirect(reverse('index'))
    return redirect(reverse('index'))


@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Cart, product=product_id, user_id=request.user.id)
    product.delete()
    return redirect(reverse('product', kwargs={'product_id': product_id}))


@login_required
def remove_from_cart_index(request, product_id):
    product = get_object_or_404(Cart, product=product_id, user_id=request.user.id)
    product.delete()
    return redirect(reverse('index'))


@login_required
def cart_products(request):
    cart_items = Cart.objects.all
    return render(request, 'cart.html', {'cart_items': cart_items})


@login_required
def remove_from_cart_items(request, product_id):
    product = get_object_or_404(Cart, product=product_id, user_id=request.user.id)
    product.delete()
    return redirect('cart_items')


@login_required
def wishlist_products(request):
    wishlist_items = wishlist.objects.all
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def remove_from_wishlist_items(request, product_id):
    product = get_object_or_404(wishlist, product=product_id, user_id=request.user.id)
    product.delete()
    return redirect(reverse('wishlist_products'))


@login_required
def add_to_wishlist_index(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not wishlist.objects.filter(product=product, user_id=request.user.id).exists():
        wishlist.objects.create(product=product, user_id=request.user)
        return redirect(reverse('index'))
    return redirect(reverse('index'))


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not wishlist.objects.filter(product=product, user_id=request.user.id).exists():
        wishlist.objects.create(product=product, user_id=request.user)
        return redirect(reverse('product', kwargs={'product_id': product_id}))
    return redirect(reverse('product', kwargs={'product_id': product_id}))


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(wishlist, product=product_id, user_id=request.user.id)
    product.delete()
    return redirect(reverse('product', kwargs={'product_id': product_id}))


@login_required
def remove_from_wishlist_index(request, product_id):
    product = get_object_or_404(wishlist, product=product_id, user_id=request.user.id)
    product.delete()
    return redirect(reverse('index'))


