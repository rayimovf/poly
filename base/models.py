from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    class Meta:
        abstract = True

    about = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField()
    is_list_price = models.BooleanField()
    list_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted_at = None
        self.save()
