from django.db import models
from django.db.models.signals import pre_save, post_save
from carts.models import Cart
from ecommerce.utils import unique_order_id_generator
from billing.models import BillingProfile
import math

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=5.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id

    def update_total(self):
        self.total = math.fsum([self.shipping_total, self.cart.total])
        self.save()
        return


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_order_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_order_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
