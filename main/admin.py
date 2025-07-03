from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'name',
        'slug',
        'price',
        'discount',
        'is_available',
        'created',
        'updated',
    )
    list_filter = ('category', 'is_available', 'created', 'updated')
    list_editable = ('price', 'discount', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
