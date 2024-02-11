from django.shortcuts import get_object_or_404, render,redirect
from .models import Product
from django.views import View
from django.contrib.auth.hashers import make_password , check_password
from .models import Customers
from django.contrib import messages
from .login_required import login_required
from .otp import generate_otp
import pytz
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from .models import Order

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



class Add_to_cart(View):
    def get(self , request):
        return render(request , "view_product.html" )
    
    def post(self , request , product_id):
        subtotal = 0
        product = Product.objects.get(id=product_id)
        product_name = product.name
        product_color = product.color
        product_price = int(product.price)
        quantity = int(request.POST.get('Quantity'))
        selected_size = request.POST.get('size')
        total_price = product_price * quantity

        subtotal += total_price
        if quantity:
            quantity = int(quantity)
            cart = request.session.get('cart', [])
            updated = False

        for cart_item in cart:
            if cart_item["product_id"] == int(product.id):
                cart_item["quantity"] += quantity
                updated = True
                break
        if not updated:
            cart_item = {
                'product_id': product.id,
                'product_name':product_name,
                'product_price':int(product_price),
                'product_color':product_color,
                'quantity': quantity,
                'size': selected_size,
                "subtotal" :subtotal,
            }
            cart.append(cart_item)
        request.session["cart"] = cart
        return redirect("cart")
    

class View_cart(View):
    def get(self , request):
        cart = request.session.get("cart" , [])
        cart_items = []

        
        for cart_item in cart:
            product_id = cart_item["product_id"]
            product = Product.objects.get(id=product_id)
            product_name = cart_item["product_name"]
            product_price = cart_item["product_price"]
            product_color = cart_item["product_color"]
            product_quantity = cart_item["quantity"]
            product_size = cart_item["size"]
            product_subtotal = cart_item["subtotal"]

            cart_items.append(
                {
                    'product_id': product_id,
                    'product':product,
                    'product_name':product_name,
                    'product_price':product_price,
                    'product_color':product_color,
                    'product_quantity': product_quantity,
                    'product_size': product_size,
                    'product_subtotal':product_subtotal,
                }
            )
        context = {
        'cart': cart_items,
        }
        
        return render(request , "cart.html" , context)
    
        

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
            subject = "Password reset"
            message = f"Your otp is {otp}. this otp expiry 1 minute"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [customer.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

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
            return redirect("password_change", email=email)
        else:
            messages.error(request, "Wrong or expired OTP")
            return render(request, 'otp.html', {'email': email})



class PasswordChange(View):
    def get(self, request, email):
        customer = Customers.get_customer_by_email(email)

        # Check if the OTP verification process has been completed
        if customer and customer.otp is not None and customer.otp_expiry_time is not None:
            return render(request, 'password_change.html', {'email': email})
        else:
            messages.error(request, 'Unauthorized access. Please complete the OTP verification first.')
            return redirect('password_reset')

    def post(self, request, email):
        customer = Customers.get_customer_by_email(email)

        if not customer:
            messages.error(request, 'Invalid email or user does not exist.')
            return redirect('password_reset')

        new_password = request.POST.get('new_password')
        retype_password = request.POST.get('retype_password')

        if new_password == retype_password:
            # Check if the OTP verification process has been completed
            if customer.otp is None and customer.otp_expiry_time is None:
                # Update the password in the database
                customer.set_password(new_password)
                customer.otp = None
                customer.otp_expiry_time = None
                customer.save()
                messages.success(request, 'Password changed successfully. You can now log in with your new password.')
                return redirect('login')
            else:
                messages.error(request, 'Unauthorized access. Please complete the OTP verification first.')
                return redirect('password_reset')
        else:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'password_change.html', {'email': email})
            


@method_decorator(login_required(login_url="login") , name="dispatch")
class ConfirmOrder(View):
    def get(self , request):
        return render(request , "address.html")
    
    def post(self , request):

        cart = request.session.get("cart", [])


        customer = request.session.get("customer")

        customer_email = Customers.objects.get(id = customer)

        email = request.POST.get("email")
        phone_number = request.POST.get("tel")
        country = request.POST.get("country")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        city = request.POST.get("City")  
        state = request.POST.get("state")
        pincode = request.POST.get("pin")
        payment = request.POST.get("paymentMethod")
        for cart_item in cart:

            product_name = cart_item.get("product_name")

            product = get_object_or_404(Product , name=product_name)
           
            product_color = cart_item.get("product_color")
            product_price = int(cart_item.get("product_price"))
            product_size = cart_item.get("size")
            product_subtotal = int(cart_item.get("subtotal"))
            product_quantity = cart_item.get("quantity")

            # Create Order instance
            Order.objects.create(
                customer=customer_email,
                product=product,
                color=product_color,
                size=product_size,
                price=product_price,
                quantity=product_quantity,
                subtotal=product_subtotal,
                email=email,
                phone_number=phone_number,
                country=country,
                first_name=first_name,
                last_name=last_name,
                city=city,
                state=state,
                pincode=pincode,
                payment_type=payment,
            )


        return redirect("order_success")
       

class Order_success(View):
    def get(self, request):
        return render(request , "order_success.html")
    


def ordersPage(request):
    customer_id = request.session.get("customer")
    if customer_id:
            customer = Customers.objects.get(id=customer_id)
            if customer:
                order = Order.objects.filter(customer=customer)
                context = {'orders': order}
            else:
                messages.error(request ,"error_message': 'Order not found for this customer" )
    else:
        messages.error(request ,"error_message': 'Order not found for this customer" )
    return render(request, "orders.html", context)
    
   