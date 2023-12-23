from django.shortcuts import render,redirect
from .models import Product

def home(request):
    product = Product.objects.all()
    return render(request , 'home.html' , {'Product':product})



def address(request):
    return render(request , 'address.html')



def view_product(request):
    product = request.GET.get('name')
    view_product_details = Product.objects.filter(name=product)

    context = {
        'product_details' : view_product_details,
    }
    return render(request , 'view_product.html' , context)


def add_to_cart(request, product_id):
    if request.method == "POST":
        product = Product.objects.get(id=product_id)
        quantity = request.POST.get('Quantity')
        selected_size = request.POST.get('size')
        if quantity:
            quantity = int(quantity)
            cart = request.session.get('cart', [])
            updated = False
        
        for cart_item in cart:
            if cart_item['product_id'] == product.id:
                # If it is, update the quantity and mark as updated
                cart_item['quantity'] += quantity
                updated = True
                break
        if not updated:
            cart_item = {
                'product_id': product.id,
                'quantity': quantity,
                'size': selected_size,
            }
            cart.append(cart_item)
        request.session['cart'] = cart
    return redirect('cart')



def view_cart(request):
    cart = request.session.get('cart', [])
    cart_items = []

    subtotal = 0
    for cart_item in cart:
        product = Product.objects.get(id=cart_item['product_id'])
        quantity = cart_item['quantity']
        selected_size = cart_item['size']
        total_price = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'size': selected_size,
        })

        subtotal += total_price
    # Now, you have a list of cart items with the product details.
    # Proceed to use this list to render your cart template.

    context = {
        'cart': cart_items,
        'subtotal': subtotal,
        # ... other context data
    }
    return render(request, 'cart.html', context)

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        # Remove the product with the given product_id from the cart
        cart = [item for item in cart if item['product_id'] != int(product_id)]
        request.session['cart'] = cart
    return redirect('cart')








