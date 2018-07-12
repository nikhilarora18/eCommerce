from django.db import models
import os
import random
from .utils import unique_slug_generator
from django.db.models.signals import pre_save , post_save
from django.urls import reverse

def get_filename_ext(filepath):
    basename=os.path.basename(filepath)
    name , ext=os.path.splitext(basename)
    return ext

def upload_image_path(instance, filename):
    new_filename=random.randint(1,39857958799)
    ext=get_filename_ext(filename)
    final_filename=f'{new_filename}{ext}'#.format(new_filename=new_filename,ext=ext)
    return "products/{new_filename}/{final_filename}".format(new_filename=new_filename,final_filename=final_filename)

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    def featured(self):
        return self.filter(featured=True,active=True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def featured(self):
        return self.get_queryset().featured()

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self,id):
        qs=self.get_queryset().filter(id=id)
        if qs.count()==1:
            return qs.first()
        return None



class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(default='abc',blank=True, unique=True)
    description=models.TextField()
    price=models.DecimalField(default=39.99,max_digits=20,decimal_places=2)
    image = models.ImageField(null=True,blank=True,upload_to=upload_image_path)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    objects=ProductManager()

    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug=self.slug)
        return reverse('products:details', kwargs={"slug":self.slug})

    def __str__(self):
        return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)