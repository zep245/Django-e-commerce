from django.shortcuts import render,redirect
from .models import *

def home(request):
    product = Product.objects.all()
    sizes = Sizes.objects.all()
    colors = Colors.objects.all()
    return render(request , 'home.html' , {'Product':product  , 'Sizes':sizes , 'Colors':colors})


def add_to_cart(request, product_id):
    if request.method == "POST":
        product = Product.objects.get(id=product_id)
        color = request.POST.get('colors')
        size = request.POST.get('sizes')
        quantity = int(request.POST.get('Quantity'))

        print(product.id)

        cart_item = {
            'product_id':product.id,
            'color': color,
            'size': size,
            'quantity': quantity,
        }
        cart = request.session.get('cart', [])
        cart.append(cart_item)
        request.session['cart'] = cart
    return redirect('home')



def view_cart(request):
    cart = request.session.get('cart', [])
    cart_items = []

    subtotal = 0
    for cart_item in cart:
        product = Product.objects.get(id=cart_item['product_id'])
        quantity = cart_item['quantity']
        total_price = product.price * quantity
        cart_items.append({
            'product': product,
            'color': cart_item['color'],
            'size': cart_item['size'],
            'quantity': quantity,
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







