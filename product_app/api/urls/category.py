from django.urls import path
from ..views.category import ListCategoryView, AddCategoryView, UpdateCategoryView, DeleteCategoryView

urlpatterns = [
    path("", ListCategoryView.as_view(), name="get-category"),
    path("add/", AddCategoryView.as_view(), name="add-category"),
    path("update/<int:category_id>/", UpdateCategoryView.as_view(), name="update-category"),
    path("delete/<int:category_id>/", DeleteCategoryView.as_view(), name="delete-category"),
]