from django import template

from cart.logic import Cart

register = template.Library()


@register.filter
def get_quantity(cart: Cart, product):
    return cart.get_quantity(product)
