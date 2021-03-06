import random

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.cache import cache_page, never_cache
from mainapp.models import *


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'categories'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu

    return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category_item = cache.get(key)
        if category_item is None:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category_item)
        return category_item

    return get_object_or_404(ProductCategory, pk=pk)


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_product):
    products_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).select_related()[:3]
    return products_list


def index(request):
    context = {
        'title': 'Главная',
        'products': Product.objects.all()[:4],
    }
    return render(request, 'mainapp/index.html', context)


def contact(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'mainapp/contact.html', context)


@cache_page(3600)
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
        }

        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = random.sample(list(Product.objects.all()), 1)[0]
    same_products = get_same_products(hot_product)
    context = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    links_menu = ProductCategory.objects.all()
    context = {
        'links_menu': links_menu,
        'product': get_object_or_404(Product, pk=pk),
    }

    return render(request, 'mainapp/product.html', context)
