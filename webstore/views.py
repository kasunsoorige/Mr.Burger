
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .forms import AddMenuForm, ShippingForm
from .models import Menu,ShippingDetails,Order,OrderItem
# Create your views here.

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



def place_order(request):
    cart = request.session.get('cart', {})  # Fetch the cart from session
    total_price = sum(float(item['price']) * int(item['quantity']) for item in cart.values())

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            # Step 1: Create a new Order
            order = Order.objects.create(total_price=total_price)

            # Step 2: Save each item in the cart as an OrderItem
            for item_id, item_data in cart.items():
                try:
                    menu_item = Menu.objects.get(id=item_id)  # Get the item from the Menu model
                    OrderItem.objects.create(
                        order=order,
                        item=menu_item,  # ForeignKey to Menu
                        quantity=item_data['quantity']
                    )
                except Menu.DoesNotExist:
                    messages.error(request, f"Item with id {item_id} does not exist.")
                    return redirect('cart')

            # Step 3: Save the shipping details
            shipping_details = form.save(commit=False)
            shipping_details.order = order  # Link shipping details to the order
            shipping_details.save()

            # Step 4: Clear the cart after order is placed
            request.session['cart'] = {}
            request.session['total_price'] = 0

            # Step 5: Success message and redirect
            messages.success(request, "Your order has been placed successfully!")
            return redirect('order_success')
        else:
            messages.error(request, "There was an error with your shipping details.")
    else:
        form = ShippingForm()

    return render(request, 'shipping_form.html', {
        'form': form,
        'total_price': total_price
    })



def order_success(request):
    return render(request, 'order_success.html')