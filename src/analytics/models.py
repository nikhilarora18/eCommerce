from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save
from accounts.signals import user_logged_in

from .signals import object_viewed_signal
from .utils import get_client_ip

User = settings.AUTH_USER_MODEL

FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_USER_ENDSESSION = getattr(settings, 'FORCE_INACTIVE_USER_ENDSESSION', False)


class ObjectViewed(models.Model):
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.CASCADE)  # it gives the user instance, Blank and null is true to record views of not signed user
    ip_address = models.CharField(max_length=220, blank=True, null=True)  # IP field can also be used
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # selects the type of model
    object_id = models.PositiveIntegerField()  # selects the id of choosen model
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s viewed on %s" % (self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']  # last viewed comes first
        verbose_name = 'object_viewed'
        verbose_name_plural = 'objects_viewed'


def object_viewed_reciever(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)  # same as instance.__class__
    if request.user.is_authenticated:
        new_viewed_object = ObjectViewed.objects.create(
            user=request.user,
            content_type=c_type,
            object_id=instance.id,
            ip_address=get_client_ip(request)
        )
    else:
        new_viewed_object = ObjectViewed.objects.create(
            #user=request.user,
            content_type=c_type,
            object_id=instance.id,
            ip_address=get_client_ip(request)
        )



object_viewed_signal.connect(object_viewed_reciever)


class UserSession(models.Model):
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.CASCADE)  # it gives the user instance, Blank and null is true to record views of not signed user
    ip_address = models.CharField(max_length=220, blank=True, null=True)  # IP field can also be used
    session_key = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended


def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        # this is to limit only 1 session per user, we can also increase the limit
        qs = UserSession.objects.filter(user=instance.user, ended=False).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()


if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=UserSession)


def post_save_user_changed_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        if not instance.is_active:
            qs = UserSession.objects.filter(user=instance.user, ended=False, active=False)
            for i in qs:
                i.end_session()


if FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_user_changed_receiver, sender=User)


def user_logged_in_reciever(sender, instance, request, *args, **kwargs):
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key,
    )


user_logged_in.connect(user_logged_in_reciever)
