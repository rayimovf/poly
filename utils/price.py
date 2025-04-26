from decimal import Decimal, InvalidOperation

def calculate_price(status, list_price, total_price, quantity):
    if status:
        total_price = list_price * quantity
    else:
        list_price = total_price / quantity if quantity else Decimal('0.0')
    return list_price, total_price


def get_price_values(request, quantity, material=None):
    try:
        status_raw = request.data.get('is_list_price')
        if status_raw is None and material:
            status = material.is_list_price
        else:
            status = str(status_raw).lower() in ['true', '1', 'yes']

        # list_price
        list_price_str = request.data.get('list_price')
        if list_price_str is None and material:
            list_price = material.list_price
        else:
            list_price = Decimal(list_price_str or '0')

        # total_price
        total_price_str = request.data.get('total_price')
        if total_price_str is None and material:
            total_price = material.total_price
        else:
            total_price = Decimal(total_price_str or '0')

        list_price, total_price = calculate_price(
            status=status,
            list_price=list_price,
            total_price=total_price,
            quantity=quantity
        )
        return list_price, total_price

    except (InvalidOperation, Exception) as error:
        return None, None
