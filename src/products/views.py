from django.shortcuts import render
from django.views.generic import ListView , DetailView
from .models import Product

class ProductFeaturedListView(ListView):
    #queryset=Product.objects.all()
    template_name="products/list.html"

    def get_queryset(self,*args,**kwargs):
        request=self.request
        return Product.objects.featured()

class ProductFeaturedDetailView(DetailView):
    #queryset=Product.objects.all()
    template_name="products/featured-detail.html"
    def get_query_set(self,*args,**kwargs):
        request=self.request
        return Product.objects.featured()

class ProductListView(ListView):
    #queryset=Product.objects.all()
    template_name="products/list.html"

    def get_queryset(self,*args,**kwargs):
        request=self.request
        return Product.objects.all()

class ProductDetailView(DetailView):
    queryset=Product.objects.all()
    template_name="products/detail.html"

class ProductDetailSlugView(DetailView):
    queryset=Product.objects.all()
    template_name="products/detail.html"
    def get_object(self,*args,**kwargs):
        request=self.request
        slug=self.kwargs.get('slug')
        try:
            instance=Product.objects.get(slug=slug,active=True)
        except Product.DoesNotExist:
            raise Http404("not found")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug,active=True)
            instance=qs.first()
        except:
            raise Http404("ummmmh")
        return instance
