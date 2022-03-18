from .models import Order


def order_item_count(request):
    item_count = Order.get_or_create_order(request)[1].items.count()
    return {'number_of_order_items': item_count}
