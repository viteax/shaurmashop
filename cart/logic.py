from django.conf import settings

from main.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def add(self, product, quantity=1, override_quantity=False):
        if product.id not in self.cart:
            self.cart[product.id] = {
                'quantity': 0,
                'price': str(product.get_price()),
            }

        if override_quantity:
            self.cart[product.id]['quantity'] = quantity
        else:
            self.cart[product.id]['quantity'] += quantity
        self.save()

    def get_total_price(self):
        total_price = 0
        for item in self.cart.values():
            total_price += item['price']
        return total_price

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
