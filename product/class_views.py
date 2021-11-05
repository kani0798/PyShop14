from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)

from .forms import CreateProductForm, UpdateProductForm
from .models import Category, Product


class SearchListView(ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = 'results'

    def get_queryset(self):
        queryset = super().get_queryset()
        # print(self.request.GET)
        search_word = self.request.GET.get('q')
        if not search_word:
            queryset = Product.objects.none()
        else:
            queryset = queryset.filter(Q(name__icontains=search_word) |
                                       Q(description__icontains=search_word))
        return queryset



class CategoryListView(ListView):
    model = Category # Category.objects.all()
    template_name = 'home.html'
    context_object_name = 'categories'


class ProductListView(ListView):
    model = Product # Product.objects.all()
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        # print(self.kwargs)
        slug = self.kwargs.get('slug')
        queryset = queryset.filter(category__slug=slug)
        return queryset


class ProductDetailView(DetailView):
    model = Product # Product.objects.get(product_id)
    template_name = 'detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'create_product.html'
    form_class = CreateProductForm
    # context_object_name = 'product_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(self.get_form_class())
        return context


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'update_product.html'
    form_class = UpdateProductForm
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(self.get_form_class())
        return context

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'delete_product.html'
    pk_url_kwarg = 'product_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.object.category.slug
        self.object.delete()
        return redirect('list', slug)
