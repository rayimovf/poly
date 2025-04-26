from django.urls import path
from ..views.format import ListFormatView, AddFormatView, UpdateFormatView, DeleteFormatView

urlpatterns = [
    path("", ListFormatView.as_view(), name="get-format"),
    path("add/", AddFormatView.as_view(), name="add-format"),
    path("update/<int:format_id>/", UpdateFormatView.as_view(), name="update-format"),
    path("delete/<int:format_id>/", DeleteFormatView.as_view(), name="delete-format")
]