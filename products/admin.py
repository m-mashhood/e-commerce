from django.contrib import admin

from products.models import Product, Sale

# Register your models here.


admin.site.register(Sale)


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('created_on', 'modified_on')


admin.site.register(Product, ProductAdmin)
