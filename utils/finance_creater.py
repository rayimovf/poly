from finance_app.models import Expense, Income
from product_app.models import Product


def create_expense(product_id):
    product = Product.objects.get(id=product_id)
    title = f"{product.owner_phone_number}: {product.category.name}"
    amount = product.material.list_price * product.quantity

    expense = Expense(
        title=title,
        amount=amount,
        product=product
    )
    expense.save()
    return True


def create_income(product_id):
    product = Product.objects.get(id=product_id)
    title = f"{product.owner_phone_number}: {product.category.name}"
    amount = product.product.total_price
    income = Income.objects.create(
        title=title,
        amount=amount,
        product=product
    )
    income.save()
    return True