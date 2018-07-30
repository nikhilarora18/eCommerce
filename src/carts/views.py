from django.shortcuts import render,redirect
from .models import Cart
from orders.models import Order
from products.models import Product
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile

def cart_home(request):
    cart_obj, new_obj=Cart.objects.new_or_get(request)
    return render(request,'carts/home.html',{"cart":cart_obj})

def cart_update(request):
    product_id=request.POST['product_id']
    product_obj=Product.objects.get(id=product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
    else:
        cart_obj.products.add(product_obj)

    request.session['cart_items']=cart_obj.products.count()
    return redirect('cart:home')

def checkout_home(request):
    cart_obj, cart_created=Cart.objects.new_or_get(request)
    order_obj=None
    if cart_created or cart_obj.products.count()==0:
        return redirect('cart:home')
    else:
        order_obj,new_order_obj=Order.objects.get_or_create(cart=cart_obj)
    user=request.user
    billing_profile=None
    login_form=LoginForm()
    if user.is_authenticated:
        billing_profile, billing_profile_created=BillingProfile.objects.get_or_create(user=user,email=user.email)

    context={
        'billing_profile':billing_profile,
        'object': order_obj,
        'login_form':login_form
    }
    print(next)
    return render(request,'carts/checkout.html',context)