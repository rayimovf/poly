from rest_framework import status
from rest_framework.response import Response
from material_app.models import Material
from product_app.models import Category
from utils.price import get_price_values, calculate_price
from utils.render_response import render_message


def get_product_data(request):
    try:
        owner_phone_number = request.data.get('owner_phone_number')
        quantity = int(request.data.get('quantity'))
        is_list_price = request.data.get('is_list_price')
        material_id = request.data.get('material_id')
        category_id = request.data.get('category_id')

        list_price, total_price = get_price_values(request)
        if list_price is None or total_price is None:
            message = get_price_values(request)
            return message

        list_price, total_price = calculate_price(
            status=is_list_price, list_price=list_price,
            total_price=total_price, quantity=quantity)

        data = {
            "material": Material.objects.get(id=material_id),
            "category": Category.objects.get(id=category_id),
            "owner_phone_number": owner_phone_number,
            "is_list_price": is_list_price,
            "list_price": list_price,
            "total_price": total_price,
        }
        if request.data.get('owner_full_name'):
            data['owner_full_name'] = data.get('owner_full_name')
        if request.data.get('about'):
            data['about'] = data.get('about')
        if request.data.get('documentation'):
            data['documentation'] = data.get('documentation')
        if request.data.get('image'):
            data['image'] = request.data.get('image')
        return data
    except Exception as error:
        message = str(error)
        return message
