from django.shortcuts import render, redirect
from .models import Cart
from orders.models import Order
from products.models import Product
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, 'carts/home.html', {"cart": cart_obj})


def cart_update(request):
    product_id = request.POST['product_id']
    product_obj = Product.objects.get(id=product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
    else:
        cart_obj.products.add(product_obj)

    request.session['cart_items'] = cart_obj.products.count()
    return redirect('cart:home')


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart:home')
    user = request.user
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()

    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

    context = {
        'billing_profile': billing_profile,
        'object': order_obj,
        'login_form': login_form,
        'guest_form': guest_form
    }
    return render(request, 'carts/checkout.html', context)
