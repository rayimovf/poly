from .material_updater import update_material
from material_app.models import Material

def handle_material_change(product, data):
    new_material = Material.objects.get(id=data['material']['id'])
    old_material = product.material

    if new_material != old_material:
        old_material.quantity += product.quantity
        old_material.total_price = old_material.list_price * old_material.quantity
        old_material.save()
        product.material = new_material
    else:
        diff = data['quantity'] - old_material.quantity
        if diff > 0:
            update_material(old_material, quantity=diff)
        else:
            old_material.quantity += abs(diff)
            old_material.total_price = old_material.list_price * old_material.quantity
            old_material.save()