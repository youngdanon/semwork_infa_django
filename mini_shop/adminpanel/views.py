from django.shortcuts import render, redirect
from loginpage.models import CustomUser, Profile
from shoppage.models import Product
from .forms import EditUserRole, ProductForm
from django.core.exceptions import PermissionDenied


def admin_required(function):
    def wrapper(request, *args, **kwargs):
        role = CustomUser.objects.get(username=request.COOKIES.get('login')).role
        if role:
            return function(request, *args, **kwargs)
        raise PermissionDenied()

    return wrapper


@admin_required
def get_users_list(request):
    usernames = [user.username for user in CustomUser.objects.all()]
    roles = [user.role for user in CustomUser.objects.all()]

    users = [(username, role) for username, role in zip(usernames, roles)]
    context = {"users": users}
    print(context)
    return render(request=request, template_name='adminpanel/admin_main.html', context=context)


@admin_required
def user_info_request(request, username):
    user = CustomUser.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    form = EditUserRole(initial={'is_admin': user.role})
    context = {'user_profile': user_profile,
               'edit_form': form}
    if request.method == 'GET':
        return render(request=request, template_name='adminpanel/admin_edit.html', context=context)
    else:
        filled_form = EditUserRole(request.POST)
        if filled_form.is_valid():
            role = filled_form.cleaned_data.get('is_admin')
            user.role = role
            user.save()
            context['edit_form'] = filled_form
            return render(request=request, template_name='adminpanel/admin_edit.html', context=context)


def display_products_request(request):
    products = Product.objects.all()
    return render(request=request, template_name='adminpanel/products.html', context={'products': products})


def display_product_info_request(request, product_id):
    product = Product.objects.get(pk=product_id)
    context = {'name': product.name, 'description': product.description, 'price': product.price, 'type': product.type,
               'weight': product.weight}
    if request.method == 'GET':
        form = ProductForm(initial=context)
        return render(request=request, template_name='adminpanel/edit_product_card.html',
                      context={'product_edit_form': form, 'product_id': product_id})
    else:
        filled_form = ProductForm(request.POST)
        if filled_form.is_valid():
            product.name = filled_form.cleaned_data.get('name')
            product.description = filled_form.cleaned_data.get('description')
            product.price = filled_form.cleaned_data.get('price')
            product.type = filled_form.cleaned_data.get('type')
            product.weight = filled_form.cleaned_data.get('weight')
            product.save()
            return render(request=request, template_name='adminpanel/edit_product_card.html',
                          context={'product_edit_form': filled_form, 'product_id': product_id})
        else:
            return render(request=request, template_name='adminpanel/edit_product_card.html',
                          context={'product_edit_form': filled_form, 'form_errors': filled_form.errors,
                                   'product_id': product_id})


def add_product_request(request):
    if request.method == "GET":
        product_form = ProductForm()
        return render(request=request, template_name='adminpanel/add_product.html',
                      context={'addproduct_form': product_form})
    else:
        filled_form = ProductForm(request.POST)
        if filled_form.is_valid():
            name = filled_form.cleaned_data.get('name')
            description = filled_form.cleaned_data.get('description')
            price = filled_form.cleaned_data.get('price')
            type = filled_form.cleaned_data.get('type')
            weight = filled_form.cleaned_data.get('weight')
            product = Product(name=name, description=description, price=price, type=type, weight=weight)
            product.save()
            return redirect('products')
        else:
            return render(request=request, template_name='adminpanel/add_product.html',
                          context={'addproduct_form': filled_form, 'form_errors': filled_form.errors})


def delete_product_request(request, product_id):
    Product.objects.filter(pk=product_id).delete()
    return redirect('products')
