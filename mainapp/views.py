from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from basketapp.models import Basket
from mainapp.models import *
from django.shortcuts import get_object_or_404
import random


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return None


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_product):
    products_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return products_list


def index(request):
    context = {
        'title': 'Главная',
        'products': Product.objects.all()[:4],
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', context)


def contact(request):
    context = {
        'title': 'Контакты',
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', context)


def products(request, pk=None, page=1):
# def products(request, pk=None):  # через передачу GET-параметров.
    title = 'Продукты'
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().order_by('price')
            category_item = {
                'name': 'все',
                'pk': 0
            }
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk).order_by('price')

        # page = request.GET.get('p', 1)  # через передачу GET-параметров.
        paginator = Paginator(products_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category_item,
            'products': products_paginator,
            'basket': get_basket(request.user)
        }

        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = random.sample(list(Product.objects.all()), 1)[0]
    same_products = get_same_products(hot_product)
    context = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': get_basket(request.user)
    }

    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    links_menu = ProductCategory.objects.all()
    context = {
        'links_menu': links_menu,
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/product.html', context)
