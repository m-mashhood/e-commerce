from django.urls import path

from .views import (AllListProduct, CreateProduct, DeleteProduct,
                    DetailViewProduct, ListProduct, PurchaseView, ReportView,
                    UpdateProduct)

urlpatterns = [
    path('', CreateProduct.as_view(), name='create_product'),
    path('list', ListProduct.as_view(), name='list_products'),
    path('list/all', AllListProduct.as_view(), name='all_list_products'),
    path('<pk>', UpdateProduct.as_view(), name='update_product'),
    path('<pk>/delete/', DeleteProduct.as_view(), name='delete_product'),
    path('<pk>/detail/', DetailViewProduct.as_view(), name='detail_product'),
    path('<pk>/sale/', PurchaseView.as_view(), name='purchase_product'),
    path('report/', ReportView.as_view(), name='report'),
]
