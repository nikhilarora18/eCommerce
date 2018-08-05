from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

User=settings.AUTH_USER_MODEL

class BillingProfileManager(models.Manager):
    def new_or_get(self,request):
        user=request.user
        guest_email_id = request.session.get('guest_email_id')
        if user.is_authenticated:
            # login user checkout ; remembers payment stuff
            obj, created = BillingProfile.objects.get_or_create(user=user, email=user.email)
        elif guest_email_id is not None:
            # guest user checkout ; refreshs payment stuff everytime
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = BillingProfile.objects.get_or_create(
                email=guest_email_obj.email)
        else:
            pass
        return obj,created

class BillingProfile(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    email=models.EmailField()
    timestamp=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    def __str__(self):
        return self.email

    objects=BillingProfileManager()


def user_created_reciever(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)

post_save.connect(user_created_reciever,sender=User)