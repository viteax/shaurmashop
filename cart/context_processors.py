from .logic import Cart


def cart(request):
    return {'cart': Cart(request)}
