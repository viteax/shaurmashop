from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.models import Product

from .forms import CartAddProductForm
from .logic import Cart


def cart_detail(request: WSGIRequest):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def add_product_htmx(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    quantity = cart.get_quantity(product)
    return render(
        request,
        'cart/cart_controls.html',
        {'product': product, 'quantity': quantity},
    )


@require_POST
def cart_remove_one(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product, quantity=1)
    quantity = cart.get_quantity(product)
    return render(
        request,
        'cart/cart_controls.html',
        {'product': product, 'quantity': quantity},
    )


@require_POST
def add_product(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product, cd['quantity'], cd['override'])
    else:
        messages.error(request, 'error')
    return redirect('main:product_list')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


@require_POST
def clear(request):
    Cart(request).clear()
    return redirect('cart:cart_detail')
