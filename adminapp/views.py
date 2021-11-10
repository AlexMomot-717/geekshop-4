from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == "POST":
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_list'))
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'form': user_form,
    }

    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    context = {
        'object_list': ShopUser.objects.all().order_by('-is_active')
    }

    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == "POST":
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_list'))
    else:
        user_form = ShopUserAdminEditForm(instance=current_user)

    context = {
        'form': user_form,
    }

    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == "POST":
        if current_user.is_active:
            current_user.is_active = False
        else:
            current_user.is_active = True
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:user_list'))

    context = {
        'object': current_user,
    }

    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    if request.method == "POST":
        category_form = ProductCategory(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_list'))
    else:
        category_form = ProductCategory()

    context = {
        'category_form': category_form,
    }

    return render(request, 'adminapp/categories.html', context)


def categories(request):
    context = {
        'object_list': ProductCategory.objects.all().order_by('-is_active')
    }

    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    current_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == "POST":
        category_form = ProductCategoryEditForm(request.POST, request.FILES, instance=current_category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_list'))
    else:
        category_form = ProductCategoryEditForm(instance=current_category)

    context = {
        'category_form': category_form,
    }

    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    current_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == "POST":
        if current_category.is_active:
            current_category.is_active = False
        else:
            current_category.is_active = True
        current_category.save()
        return HttpResponseRedirect(reverse('adminapp:category_list'))

    context = {
        'object': current_category,
    }

    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request):
    if request.method == "POST":
        product_form = Product(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('adminapp:product_list'))
    else:
        product_form = Product()

    context = {
        'product_form': product_form,
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    context = {
        'category': get_object_or_404(ProductCategory, pk=pk),
        'object_list': Product.objects.filter(category__pk=pk).order_by('-is_active')
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    context = {

    }

    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request):
    context = {

    }

    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def product_detail(request, pk):

    context = {
        'product': get_object_or_404(Product, pk=pk),
        'object_list': Product.objects.filter(pk=pk).order_by('-is_active')
    }

    return render(request, 'adminapp/product_detail.html', context)

