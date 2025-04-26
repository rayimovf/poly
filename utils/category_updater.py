from product_app.models import Category

def update_category(category, quantity, total_price):
    """Helper function to update category quantity and total price."""
    category.quantity += quantity
    category.total_price += total_price
    category.save()


def handle_category_change(product, data):
    """Helper function to handle category change."""
    old_category = Category.objects.get(id=product.category.id)
    new_category = Category.objects.get(data['category']['id'])
    old_total_price = product.total_price
    new_total_price = data['total_price']
    if new_category != old_category.id:
        old_category.quantity -= 1
        old_category.total_price -= product.total_price
        old_category.save()

        update_category(category=new_category, quantity=1, total_price=data['total_price'])
        product.category = new_category
    else:
        price_difference = new_total_price - old_total_price
        update_category(category=old_category, quantity=0, total_price=price_difference)
    product.save()