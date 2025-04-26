from django_filters import rest_framework as filters
from .models import Material

class MaterialFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    format_name = filters.CharFilter(field_name='format__name', lookup_expr='icontains')
    is_active = filters.BooleanFilter(field_name='is_active')
    created_at = filters.DateFromToRangeFilter(field_name='created_at', lookup_expr='gte')

    class Meta:
        model = Material
        fields = ['name', 'format__name', 'is_active', 'created_at']