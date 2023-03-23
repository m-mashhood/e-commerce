from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)

from users.models import User

from .forms import ProductForm, ProductRetailerForm
from .models import Product, Sale


class CreateProduct(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('list_products')
    template_name = 'product.html'

    def get_form_class(self):
        if self.request.user.category == User.RETAILER[0]:
            return ProductRetailerForm
        else:
            return ProductForm

    def form_valid(self, form):
        form.instance.owned_by = self.request.user
        return super().form_valid(form)


class UpdateProduct(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    form_class = ProductForm
    success_url = reverse_lazy('list_products')
    template_name = 'product.html'
    queryset = Product.objects.all()


class ListProduct(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Product
    paginate_by = 6
    context_object_name = 'products'
    template_name = 'listproduct.html'

    def get_queryset(self):
        return Product.objects.filter(owned_by=self.request.user)


class DeleteProduct(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Product
    success_url = reverse_lazy('list_products')
    template_name = 'confirmdelete.html'


class AllListProduct(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Product
    paginate_by = 6
    context_object_name = 'products'
    template_name = 'all_list_products.html'

    def get_queryset(self):
        if self.request.user.category == User.RETAILER[0]:
            return Product.objects.filter(owned_by__category=User.VENDOR[0])
        elif self.request.user.category == User.BUYER[0]:
            return Product.objects.filter(owned_by__category=User.RETAILER[0])
        else:
            return Product.objects.none()


class DetailViewProduct(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Product
    context_object_name = 'product'
    template_name = 'product_detail.html'


class PurchaseView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def post(self, request, pk):
        data = request.POST

        product = Product.objects.get(id=pk)
        product.in_stock -= int(data['quantity'])
        product.save()

        Sale.objects.create(
            product=product,
            buyer=request.user,
            seller=product.owned_by,
            purchased_quantity=int(data['quantity']),
            selling_price=float(data.get('selling_price', 0)),
            purchase_price=product.latest_price
        )

        if request.user.category == User.RETAILER[0]:
            existing_product = Product.objects.filter(owned_by=request.user, key=product.key).first()

            if existing_product:
                existing_product.in_stock += int(data['quantity'])
                existing_product.latest_price = float(data['selling_price'])
                existing_product.save()
            else:
                Product.objects.create(
                    name=product.name,
                    category=product.category,
                    unit=product.unit,
                    picture=product.picture,
                    description=product.description,
                    in_stock=int(data['quantity']),
                    owned_by=request.user,
                    bought_on=timezone.now(),
                    latest_price=float(data['selling_price']),
                    key=product.key,
                )

        if request.user.category == User.RETAILER[0]:
            return redirect('list_products')
        else:
            return redirect('all_list_products')


class ReportView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'report.html'

    def get(self, request):
        products = self.get_products()
        context = self.get_context(products)
        return render(request, self.template_name, context=context)

    def post(self, request):
        data = request.POST
        start = data.get('start')
        end = data.get('end')
        products = self.get_products()
        context = self.get_context(products, start, end)
        return render(request, self.template_name, context=context)

    def get_products(self):
        return Product.objects.filter(owned_by=self.request.user)

    def get_sales_set(self, product_key, start, end, is_buyer=False):
        sales = Sale.objects.filter(product__key=product_key, seller=self.request.user)

        if is_buyer:
            sales = Sale.objects.filter(product__key=product_key, buyer=self.request.user)

        if start:
            start = datetime.strptime(start, '%Y-%m-%d')
            start = datetime.combine(start.date(), datetime.min.time())
            sales = sales.filter(created_on__gte=start)

        if end:
            end = datetime.strptime(end, '%Y-%m-%d')
            end = datetime.combine(end.date(), datetime.max.time())
            sales = sales.filter(created_on__lte=end)

        return sales

    def get_context(self, products, start=None, end=None):
        context = {
            'objects': [],
            'total': {
                'product_stock': 0,
                'purchase_qty': 0,
                'purchase_price': 0,
                'sold_qty': 0,
                'sold_price': 0,
                'profit': 0
            },
            'start': start,
            'end': end
        }

        for product in products:
            sale_set = self.get_sales_set(product.key, start, end)
            purchase_set = self.get_sales_set(product.key, start, end, is_buyer=True)
            purchase = purchase_set.first()

            data = {
                'product_name': product.name, 'product_category': product.get_category_display(),
                'product_stock': product.in_stock,
                'purchase_qty': purchase_set.aggregate(Sum('purchased_quantity', default=0))['purchased_quantity__sum'],
                'purchase_price': purchase.purchase_price if purchase else 0,
                'sold_qty': sale_set.aggregate(Sum('purchased_quantity', default=0))['purchased_quantity__sum'],
                'sold_price': sale_set.aggregate(total=Sum(F('purchase_price') * F('purchased_quantity'),
                                                           default=0))['total']
            }

            data['profit'] = data['sold_price'] - (data['sold_qty'] * data['purchase_price'])
            context['objects'].append(data)

        for product in context['objects']:
            context['total']['product_stock'] += product['product_stock']
            context['total']['purchase_qty'] += product['purchase_qty']
            context['total']['purchase_price'] += product['purchase_price']
            context['total']['sold_qty'] += product['sold_qty']
            context['total']['sold_price'] += product['sold_price']
            context['total']['profit'] += product['profit']

        return context
