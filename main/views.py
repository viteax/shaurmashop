from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm

from .models import Category, Product


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    add_product_form = CartAddProductForm()

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(
        request,
        'main/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
            'add_product_form': add_product_form,
        },
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    return render(
        request,
        'main/product/detail.html',
        {
            'product': product,
            'related_products': related_products,
        },
    )
