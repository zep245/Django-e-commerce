from .models import Product

def num_items_in_cart(request):
    cart = request.session.get('cart', [])
    return {'num_items_in_cart': len(cart)}
