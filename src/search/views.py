from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product

class SearchProductView(ListView):
    template_name="search/view.html"

    def get_queryset(self,*args,**kwargs):
        request=self.request
        method_dict=request.GET           #it creates a python dictionary
        query=method_dict.get('q')
        if query is not None:
            return Product.objects.filter(title__icontains=query)
        else:
            return Product.objects.all()