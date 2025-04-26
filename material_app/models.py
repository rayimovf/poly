from django.db import models
from base.models import BaseModel


class Format(models.Model):
    name = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    gram = models.PositiveIntegerField()
    type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}: {self.gram}"


class Material(BaseModel):
    name = models.CharField(max_length=255)
    format = models.ForeignKey(Format, on_delete=models.CASCADE)
    is_active = models.BooleanField()

    def __str__(self):
        return f"{self.name}: {self.format.name}"

    @classmethod
    def fetch_available_materials(cls):
        return cls.objects.filter(deleted_at__isnull=True)

    @classmethod
    def fetch_inactive_materials(cls):
        return cls.objects.filter(deleted_at__isnull=False)
