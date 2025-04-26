

def update_material(material, quantity):
    """Helper function to update material quantity and total price."""
    if material.quantity < quantity:
        return False

    material.quantity -= quantity
    material.total_price = material.list_price * quantity

    if material.quantity == 0:
        material.is_active = False
    material.save()
    return True
