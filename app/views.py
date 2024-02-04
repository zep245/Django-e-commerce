from django.shortcuts import render,redirect
from .models import Product
from django.views import View
from django.contrib.auth.hashers import make_password , check_password
from .models import Customers
from django.contrib import messages
from .login_required import login_required
from .otp import generate_otp
import pytz
from datetime import datetime, timedelta

def home(request):
    product = Product.objects.all()
    return render(request , 'home.html' , {'Product':product})




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


@login_required(login_url="login")
def address(request):
    cart = request.session.get("cart", [])

    subtotal = 0
    for cart_item in cart:
        product = Product.objects.get(id=cart_item['product_id'])
        quantity = cart_item['quantity']
        total_price = product.price * quantity
    

        subtotal += total_price

    context = {
        'subtotal': subtotal,
    }
    return render(request, 'address.html', context )


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        # Remove the product with the given product_id from the cart
        cart = [item for item in cart if item['product_id'] != int(product_id)]
        request.session['cart'] = cart
    return redirect('cart')





class Signup(View):
    def get(self , request):
        return render(request , 'register.html')


    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get("password2")


        if len(password and password2) < 8:
            messages.error(request , 'Password must be at least 8 characters long.')
            return redirect("register")

        if password != password2:
            messages.error(request , "Password not match try again.")
            return redirect('register')
        
        if Customers.objects.filter(email=email).exists():
            messages.error(request , 'This email is already registered. Please use a different email.')
            return redirect('register')
        
        if not password[0].isupper():
            messages.error(request , 'Password must start with a capital letter.')
            return redirect('register')
            
        Customers.objects.create(email=email , password = make_password(password))
        return redirect('login')
    

        
class Login(View):

    def get(self , request):
        return render(request , 'login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customers = Customers.get_customer_by_email(email)

        if customers:
            if check_password(password, customers.password):
                request.session['customer'] = customers.id
                print(request.session) 
                return redirect('home') 
            else:
                messages.error(request, 'Invalid password')
        else:
            messages.error(request, 'Customer not found')

        return render(request, 'login.html', {'customers': customers})
    

class Logout(View):
    def get(self, request):
        # Use pop to remove the 'customer' key from the session
        request.session.pop('customer', None)
        return redirect('login')
    


    
class PasswordReset(View):
    def get(self, request):
        return render(request, 'password_reset.html')

    def post(self, request):
        email = request.POST.get("password_reset_email")
        customer = Customers.get_customer_by_email(email)

        if customer:
            otp = generate_otp()
            print(otp)
            customer.otp = otp
            ist = pytz.timezone('Asia/Kolkata')
            customer.otp_expiry_time = datetime.now(ist) + timedelta(seconds=60)  # Set OTP expiry time (adjust as needed)
            
            customer.save()

            # Send OTP to the user (e.g., via email or SMS)

            return redirect("otp", email=email)
        else:
            messages.error(request, "The email is not found")
            return redirect("password_reset")

class OtpSystem(View):
    def get(self, request, email=None):
        if email:
            return render(request, 'otp.html', {'email': email})
        else:
            messages.error(request, 'Email parameter is missing.')
            return redirect('password_reset')

    def post(self, request , email=None):
        if not email:
            messages.error(request, 'Email parameter is missing.')
            return redirect('password_reset')

        customer = Customers.get_customer_by_email(email)

        if not customer:
            messages.error(request, 'Invalid email or user does not exist.')
            return redirect('password_reset')

        otp_values = [
            request.POST.get('otp1'),
            request.POST.get('otp2'),
            request.POST.get('otp3'),
            request.POST.get('otp4'),
            request.POST.get('otp5'),
            request.POST.get('otp6'),
        ]

        if None in otp_values or '' in otp_values:
            messages.error(request, 'Please enter the complete OTP')
            return render(request, 'otp.html', {'email': email})
        else:
            user_otp = ''.join(otp_values)

        customer_otp_expiry_time_utc = customer.otp_expiry_time.replace(tzinfo=pytz.UTC)

        # Convert customer.otp_expiry_time_utc to IST
        ist = pytz.timezone('Asia/Kolkata')
        customer_otp_expiry_time_ist = customer_otp_expiry_time_utc.astimezone(ist)

        if customer.otp == int(user_otp) and customer_otp_expiry_time_ist > datetime.now(ist):
            messages.success(request, "Success")
            # Clear the OTP information from the database
            customer.otp = None
            customer.otp_expiry_time = None
            customer.save()
            return redirect("password_change", email=email)
        else:
            messages.error(request, "Wrong or expired OTP")
            return render(request, 'otp.html', {'email': email})


            
class PasswordChange(View):
    def get(self, request, email):
        return render(request, 'password_change.html', {'email': email})

    def post(self, request, email):
        customer = Customers.get_customer_by_email(email)

        if not customer:
            messages.error(request, 'Invalid email or user does not exist.')
            return redirect('password_reset')

        new_password = request.POST.get('new_password')
        retype_password = request.POST.get('retype_password')

        if new_password == retype_password:
            # Update the password in the database
            customer.set_password(new_password)
            customer.save()

            messages.success(request, 'Password changed successfully. You can now log in with your new password.')
            return redirect('login')  # Redirect to the login page or any other desired page
        else:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'password_change.html', {'email': email})
            



