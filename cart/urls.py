from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>', views.add_product, name='add_product'),
    path('remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('clear', views.clear, name='clear'),
    path(
        'add/<int:product_id>/htmx/',
        views.add_product_htmx,
        name='add_product_htmx',
    ),
    path(
        'remove_one/<int:product_id>',
        views.cart_remove_one,
        name='cart_remove_one',
    ),
]
