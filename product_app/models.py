from django.db import models
from base.models import BaseModel
from material_app.models import Material


class Category(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Product(BaseModel):
    owner_full_name = models.CharField(max_length=255, null=True, blank=True)
    owner_phone_number = models.CharField(max_length=255)
    documentation = models.FileField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    @classmethod
    def fetch_available_products(cls):
        return cls.objects.filter(deleted_at__isnull=False)

    @classmethod
    def fetch_inactive_products(cls):
        return cls.objects.filter(deleted_at__isnull=True)

    def __str__(self):
        return f"{self.owner_phone_number}: {self.category.name}"
