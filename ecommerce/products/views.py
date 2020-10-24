from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.http import Http404
from django.views.generic.detail import DetailView

from .models import Product


class ProductFeaturedListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.features()

class ProductFeaturedDetailView(DetailView):
    template_name = "products/featured_details.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.features()

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/details.html"

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        instance = get_object_or_404(Product, slug=slug, active=True)
        # if instance is None:
        #     raise Http404("Product doesn't exist")
        return instance
class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return Product.objects.all()
    
class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/details.html"


    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance