from django.db import models
from product_app.models import Product


class Expense(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount}, {self.product.category.name}"

    def delete(self):
        self.delete()
        return True


class Income(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount}, {self.product.category.name}"

    def delete(self):
        self.delete()
        return True