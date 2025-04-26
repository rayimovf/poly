from django.urls import path
from ..views.material import (
    ListMaterialView, SingleMaterialView, AddMaterialView,
    UpdateMaterialView, SoftDeleteMaterialView, RestoreMaterialView,
    DeleteMaterialView, FilterMaterialView
)
urlpatterns = [
    path("", ListMaterialView.as_view(), name="get-material"),
    path("single/<int:material_id>/",SingleMaterialView.as_view(), name="single-material"),
    path("add/", AddMaterialView.as_view(), name="add-material"),
    path("update/<int:material_id>/", UpdateMaterialView.as_view(), name="update-material"),
    path("soft-delete/<int:material_id>/", SoftDeleteMaterialView.as_view(), name="soft-delete-material"),
    path("restore/<int:material_id>/", RestoreMaterialView.as_view(), name="restore-material"),
    path("delete/<int:material_id>/", DeleteMaterialView.as_view(), name="delete-material"),
    path("filter/", FilterMaterialView.as_view(), name="filter-material"),
]

