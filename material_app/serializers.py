from rest_framework import serializers
from .models import Format, Material


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = '__all__'


class MaterialListSerializer(serializers.ModelSerializer):
    format = FormatSerializer(read_only=True)

    class Meta:
        model = Material
        fields = (
            "id", "name", "format", "quantity",
            "total_price", "is_active", "created_at"
        )


class MaterialSerializer(serializers.ModelSerializer):
    format = FormatSerializer(read_only=True)
    format_id = serializers.PrimaryKeyRelatedField(
        queryset=Format.objects.all(), source='format', write_only=True)

    class Meta:
        model = Material
        fields = (
            "name", "about", "quantity", "is_list_price",
            "list_price", "total_price", "is_active", "image",
            "format", "format_id", "created_at", "updated_at",
            "deleted_at", "id"
        )