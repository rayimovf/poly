from django.urls import path
from ..views.product import ListProduct, DetailProductView, AddProductView, UpdateProductView, \
    SoftDeleteProductView, RestoreProductView, DeleteProductView

urlpatterns = [
    path("", ListProduct.as_view(), name='get-product'),
    path("detail/<int:product_id>/", DetailProductView.as_view(), name='detail-product'),
    path("add/", AddProductView.as_view(), name='add-product'),
    path("update/<int:product_id>/", UpdateProductView.as_view(), name='update-product'),
    path("soft-delete/<int:product_id>/", SoftDeleteProductView.as_view(), name='soft-delete-product'),
    path("restore/<int:product_id>/", RestoreProductView.as_view(), name='restore-product'),
    path("delete/<int:product_id>/", DeleteProductView.as_view(), name='delete-product'),
]