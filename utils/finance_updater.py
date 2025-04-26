from finance_app.models import Expense, Income


def update_expense(product):
    expense = Expense.objects.get(product_id=product.id)
    expense.title = f"{product.owner_phone_number}: {product.category}"
    expense.amount = product.material.list_price * product.quantity
    expense.save()

def update_income(product):
    income = Income.objects.get(product_id=product.id)
    income.title = f"{product.owner_phone_number}: {product.category}"
    income.amount = product.total_price
    income.save()
