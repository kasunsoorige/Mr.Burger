
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .forms import AddMenuForm, ShippingForm
from .models import Menu,ShippingDetails,Order,OrderItem
from .models import Menu
from .models import Order
from .models import Reservation
from django.views.decorators.csrf import csrf_exempt
from .models import Notification, Order
from .models import Order
from .forms import OrderForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import UserProfile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import UserProfile

# Create your views here.

@login_required
def my_orders(request):
    # Fetch orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'my_orders.html', {'orders': orders})




def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'myapp/register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'myapp/register.html', {'form': form})



from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout



@login_required
def my_orders(request):
    # Fetch orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'my_orders.html', {'orders': orders})




def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'myapp/register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'myapp/register.html', {'form': form})



from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout



def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
            # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('dash')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:        
        return render(request,'home.html', {})

def dash(request):
    return render(request,'base_dash.html',
                        {})


def add_menu(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddMenuForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()  # Save the form (no need to assign `add_menu`)
                messages.success(request, "Menu is Added...")
                return redirect('dash')
            else:
                # If form is not valid, render the form with errors
                messages.error(request, "Error adding menu. Please check the form.")
                return render(request, 'add_menu.html', {'form': form})
        else:
            # If GET request, render an empty form
            form = AddMenuForm()
            return render(request, 'add_menu.html', {'form': form})
    else:

        messages.error(request, "You Must Be Logged In...")
        return redirect('home')


#### Items view of the page

def item_list(request):
    items = Menu.objects.all()
    return render(request, 'item_list.html', {'items': items})


def add_to_cart(request, item_id):
    item = get_object_or_404(Menu, id=item_id)
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] += 1
    else:
        cart[str(item_id)] = {
            'item_id': item_id,
            'name': item.name,
            'price': str(item.price),
            'quantity': 1,
            'image_url': item.img_url.url,  
        }

    request.session['cart'] = cart
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    total_price = sum(float(item['price']) * int(item['quantity']) for item in cart.values())
    
    # Set total_price in the session
    request.session['total_price'] = total_price

    return render(request, 'cart.html', {
        'cart': cart,
        'total_price': total_price
    })  

def update_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity'))

        if item_id in cart:
            cart[item_id]['quantity'] = quantity

        request.session['cart'] = cart

        # Recalculate total price
        total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())
        item_total_price = float(cart[item_id]['price']) * cart[item_id]['quantity']

        return JsonResponse({
            'total_price': total_price,
            'item_total_price': item_total_price,
        })
    #return JsonResponse({'error': 'Invalid request'}, status=400)   
    else:   
        messages.error(request, "invalid")
        return redirect('item_list') 

def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cart = request.session.get('cart', {})

            # Remove the item from the cart if it exists
        if item_id in cart:
            del cart[item_id]
            request.session['cart'] = cart  # Update session

            # Calculate new total price after removal
            total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())

            # Return updated total price as JSON response
        return JsonResponse({'total_price': total_price})
    else:    
        messages.error(request, "Please add items to cart...")
        return redirect('item_list')



from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Order, OrderItem, Menu
from .forms import ShippingForm

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Order, OrderItem, Menu
from .forms import ShippingForm

def place_order(request):
    # Get the cart from the session
    # Get the cart from the session
    cart = request.session.get('cart', {})
    total_price = sum(float(item['price']) * int(item['quantity']) for item in cart.values())
    
    

    # Check if the cart is empty
    
    

    # Check if the cart is empty
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            # Create a new Order with total_price and the logged-in user
            order = Order.objects.create(
                total_price=total_price,
                user=request.user if request.user.is_authenticated else None  # Associate the user if logged in
                
            )
            # Create a new Order with total_price and the logged-in user
            order = Order.objects.create(
                total_price=total_price,
                user=request.user if request.user.is_authenticated else None  # Associate the user if logged in
                
            )

            # Save each item in the cart as an OrderItem
            for item_id, item_data in cart.items():
                try:
                    menu_item = Menu.objects.get(id=item_id)
                    OrderItem.objects.create(
                        order=order,
                        item=menu_item,
                        quantity=item_data['quantity']
                    )
                except Menu.DoesNotExist:
                    messages.error(request, f"Item with id {item_id} does not exist.")
                    return redirect('cart')

            # Save the shipping details
            shipping_details = form.save(commit=False)
            shipping_details.order = order
            shipping_details.save()

                        # Update loyalty points for the user
            if request.user.is_authenticated:
                user_profile = UserProfile.objects.get(user=request.user)
                loyalty_points = total_price * 0.05  # 5% of the order amount
                user_profile.loyalty_points += loyalty_points
                user_profile.save()

                        # Update loyalty points for the user
            if request.user.is_authenticated:
                user_profile = UserProfile.objects.get(user=request.user)
                loyalty_points = total_price * 0.05  # 5% of the order amount
                user_profile.loyalty_points += loyalty_points
                user_profile.save()

            # Clear the cart after order is placed
            request.session['cart'] = {}
            request.session['total_price'] = 0

            # Success message and redirect
            messages.success(request, "Your order has been placed successfully!")
            return redirect('order_success')  # Update with your success page view name
        else:
            messages.error(request, "There was an error with your shipping details.")
    else:
        form = ShippingForm()

    return render(request, 'shipping_form.html', {'form': form, 'total_price': total_price})

def manage_menu(request):
    items = Menu.objects.all()
    return render(request, 'manage_menu.html', {'items': items})

def edit_menu(request, item_id):
    item = get_object_or_404(Menu, id=item_id)
    if request.method == 'POST':
        form = AddMenuForm(request.POST, request.FILES, instance=item)  # Include request.FILES here
        if form.is_valid():
            form.save()
            return redirect('manage_menu')
    else:
        form = AddMenuForm(instance=item)
    return render(request, 'edit_menu.html', {'form': form})

def delete_menu(request, item_id):
    item = get_object_or_404(Menu, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('manage_menu')
    return render(request, 'delete_menu.html', {'item': item})


def order_success(request):
    return render(request, 'order_success.html')




#new

def view_orders(request):
    # Retrieve all orders
    orders = Order.objects.all()
    order_details = []

    for order in orders:
        # Fetch order items
        order_items = OrderItem.objects.filter(order=order)
        
        # Fetch shipping details for the order
        try:
            shipping_details = ShippingDetails.objects.get(order=order)
        except ShippingDetails.DoesNotExist:
            shipping_details = None  # In case shipping details are missing

        # Prepare data for display
        order_detail = {
            'order': order,
            'shipping_details': shipping_details,
            'order_items': order_items
        }
        order_details.append(order_detail)

    return render(request, 'view_orders.html', {'order_details': order_details})


def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        messages.success(request, f"Order {order_id} status updated to {new_status}.")
    return redirect('view_orders')  # Redirect back to the orders page


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reservation

from .models import  Table

from .models import  Table

def book_table(request):
    if request.method == "POST":
        # Collect reservation details from the initial form
        reservation_date = request.POST.get("reservation_date")
        reservation_time = request.POST.get("reservation_time")
        num_people = request.POST.get("num_people")
        tables = request.POST.getlist("tables")  # Get list of selected tables

        tables = request.POST.getlist("tables")  # Get list of selected tables

        # Save these details in the session temporarily
        request.session['reservation_details'] = {
            "date": reservation_date,
            "time": reservation_time,
            "num_people": num_people,
            "tables": tables,  # Store list of tables
            "tables": tables,  # Store list of tables
        }


        # Redirect to the customer details form
        return redirect('customer_details_form')

    return render(request, 'book_table.html')

def customer_details_form(request):
    if request.method == "POST":
        # Retrieve details from the session
        reservation_details = request.session.get('reservation_details', {})
        customer_name = request.POST.get('name')
        customer_email = request.POST.get('email')
        customer_phone = request.POST.get('phone')
        selected_tables = request.POST.getlist('tables')  # Get list of selected table numbers
        selected_tables = request.POST.getlist('tables')  # Get list of selected table numbers

        # Create the reservation
        reservation = Reservation.objects.create(
        # Create the reservation
        reservation = Reservation.objects.create(
            date=reservation_details.get("date"),
            time=reservation_details.get("time"),
            num_people=reservation_details.get("num_people"),
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
        )

        # Add selected tables to the reservation
        for table_number in selected_tables:
            table, created = Table.objects.get_or_create(number=table_number)
            reservation.tables.add(table)

        messages.success(request, "Your tables have been reserved!")
        # Add selected tables to the reservation
        for table_number in selected_tables:
            table, created = Table.objects.get_or_create(number=table_number)
            reservation.tables.add(table)

        messages.success(request, "Your tables have been reserved!")
        return redirect('reservation_success')

    return render(request, 'customer_details_form.html')


def view_reservations(request):
    date_filter = request.GET.get('date')  # Get the date from query parameters
    if date_filter:
        reservations = Reservation.objects.filter(date=date_filter)  # Filter by date
    else:
        reservations = Reservation.objects.all()  # Get all reservations

    return render(request, 'view_reservations.html', {'reservations': reservations})


def reservation_success(request):
    return render(request, 'reservation_success.html')



def admin_notifications(request):
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')
    return render(request, "admin_notification.html", {"notifications": notifications})


@csrf_exempt  # Add this line to disable CSRF protection for this view
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.is_read = True
    notification.save()
    return JsonResponse({"success": True})



from django.shortcuts import render, get_object_or_404
from .models import Order  # Make sure you have the correct import if you're using an Order model

def order_details(request, order_id):
    # Retrieve the specific order from view_orders.html
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_details.html', {'order': order})






def confirm_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'confirm_cancel.html', {'order': order})

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order.delete()
        return redirect('view_orders')  # Redirect to all orders after cancellation

    return redirect('view_orders')  # Redirect if GET request is received (optional)


def rewards(request):
    return render(request, 'rewards.html')

def rewards(request):
    loyalty_points = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        loyalty_points = user_profile.loyalty_points

    return render(request, 'rewards.html', {'loyalty_points': loyalty_points})


def about(request):
    return render(request, 'about.html')