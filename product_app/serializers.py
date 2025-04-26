from rest_framework import serializers

from material_app.models import Material
from .models import Category, Product
from material_app.serializers import MaterialListSerializer, MaterialSerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    material = MaterialListSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        modal = Product
        fields = (
            "owner_phone_number", "category", "quantity",
            "total_price", "material", "created_at", "id"
        )


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    material = MaterialListSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True)
    material_id = serializers.PrimaryKeyRelatedField(
        queryset=Material.objects.all(), source="material", write_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "owner_full_name", "owner_phone_number", "about",
            "image", "documentation", "quantity", "is_list_price",
            "list_price", "total_price", "category", "material",
            "category_id", "material_id"
        )