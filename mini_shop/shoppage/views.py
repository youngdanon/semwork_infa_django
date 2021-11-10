from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from loginpage.views import login_required
from .models import Product


# Create your views here.
@login_required
def pricing(request):
    products = [(product.pk, product.name, product.description, product.price, product.type, product.weight) for product
                in Product.objects.all()]
    context = {'products': products}
    print(context)
    return render(request, 'shoppage/pricing.html', context=context)


@login_required
def product_card_request(request, product_id):
    pass
