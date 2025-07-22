from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from main.models import Product


class Cart:
    def __init__(self, request: WSGIRequest):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart: dict[str, str] = cart

    def save(self):
        self.session.modified = True

    def remove(self, product: Product, quantity=0):
        product_id = str(product.id)
        if product_id not in self.cart:
            return

        if quantity and self.cart[product_id]['quantity'] >= quantity:
            self.cart[product_id]['quantity'] -= quantity
        else:
            del self.cart[product_id]
        self.save()

    def add(self, product: Product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.get_price()),
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def get_quantity(self, product: Product) -> int:
        info = self.cart.get(str(product.id))
        return int(info['quantity']) if info else 0

    def get_total_price(self) -> float:
        return round(
            sum(
                item['price'] * item['quantity']
                for item in self.cart.values()
            ),
            2,
        )

    def clear(self):
        del self.cart
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
