from django.shortcuts import get_object_or_404, render,redirect
from .models import Product
from django.views import View
from django.contrib.auth.hashers import make_password , check_password
from .models import Customers
from django.contrib import messages
from .login_required import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from .models import Order
from .utils import password_reset_token_generator
from django.urls import reverse

def home(request):
    product = Product.objects.all()
    return render(request , 'home.html' , {'Product':product})




def view_product(request):
    product = request.GET.get('name')
    view_product_details = Product.objects.filter(name=product)

    context = {
        'product_details' : view_product_details,
        'title':'Products',
    }
    return render(request , 'view_product.html' , context)



class Add_to_cart(View):
    def get(self , request):
        return render(request , "view_product.html")
    
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
        
        return render(request , "cart.html" , context , {'title':'Cart'})
    
        

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        # Remove the product with the given product_id from the cart
        cart = [item for item in cart if item['product_id'] != int(product_id)]
        request.session['cart'] = cart
    return redirect('cart')





class Signup(View):
    def get(self , request):
        return render(request , 'register.html' , {'title':'Register'})


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
        return render(request , 'login.html' , {'title':'Login'})
    
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
    




def passwordReset(request):
    if request.method == 'POST':
        email = request.POST.get('password_reset_email')
        user = Customers.objects.filter(email=email).first()
        if user:
            token = password_reset_token_generator.generate_token(user)
            reset_link = settings.BASE_URL + reverse('password_change' , kwargs={'token':token})
        
            # send by email
            subject = 'Password Reset'
            message = f'Please click the following link to reset your password:\n{reset_link}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            messages.success(request , "Password reset link sent to your email.")
            return redirect("password_reset")
        else:
            messages.error(request, 'No user found with that email.')
    return render(request , "password_reset.html" , {'title':'Password reset'})
        
        
    


def passwordChange(request, token):
    user_id = password_reset_token_generator.validate_token(token)
    if user_id:
        user = Customers.objects.filter(id=user_id).first()
        if user:
            if request.method == "POST":
                new_password = request.POST.get('new_password')
                retype_password = request.POST.get('retype_password')
                if new_password == retype_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password changed successfully. You can now log in with your new password.')
                    return redirect("login")
                else:
                    messages.error(request, "Passwords do not match.")
            return render(request, 'password_change.html', {'token': token})
        else:
            messages.error(request, "No user found!")
            return redirect("password_reset")
    else:
        messages.error(request, "Invalid token.")
        return redirect("password_reset" , {'title':'Password change'})


        


   




            


@method_decorator(login_required(login_url="login") , name="dispatch")
class ConfirmOrder(View):
    def get(self , request):
        cart = {
            'carts':request.session.get("cart", [])
        }
        return render(request , "address.html" , cart , {'title':'Address'})
    
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


        return render(request , "order_success.html")
       


        
    




class Order_page(View):
    def get(self ,request):
        customer_id = request.session.get("customer")
        if customer_id:
                customer = Customers.objects.get(id=customer_id)
                order = Order.objects.filter(customer=customer)
                context = {'orders': order}
        else:
            return redirect("login")
        return render(request, "orders.html", context , {'title':'Orders'})

    
   