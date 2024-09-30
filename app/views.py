# from pyexpat.errors import messages
from multiprocessing import AuthenticationError
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.shortcuts import render
from django.http import HttpResponse

from django.views import View
from .models import Product
from .models import CartItem
from .models import Wishlist
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import os
import google.generativeai as genai
from django.shortcuts import render
from .models import OrderItem, Order
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Count 
from .models import Order
from .models import Order, OrderItem





def home(request):
    products= Product.objects.all()
    return render(request,"app/home.html",{'products': products})


def about(request):
   return render(request,"about.html")


def contact(request):
    return render(request,"contact.html")

def admin_product_page(request):
    products = Product.objects.all()
    return render(request, 'admin_product_page.html', {'products': products})



def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_product_page')  # Redirect to a success page after adding the product
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_product_page')  # Redirect to the product detail page after updating
    else:
        form = ProductUpdateForm(instance=product)
    return render(request, 'update_product.html', {'form':form, 'product':product})


    
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_product_page')  # Redirect to the product list page after deletion
    return render(request, 'delete_product.html', {'product': product})



def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_superuser:
                auth_login(request, user)
                #return redirect('admin_product_page')
                return redirect('admin_dashboard')
            else:
                return render(request, 'admin_login.html', {'form': form, 'error_message': 'Invalid credentials'})

    else:
        form = AuthenticationError()

    return render(request, 'admin_login.html', {'form': form})


def custom_logout_view(request):
    logout(request)  # This logs out the user
    return redirect('home')


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'app/product_details.html', {'product': product})

@login_required(login_url='login')
def add_to_cart(request, id):
    prod = get_object_or_404(Product, id=id)
    cart_item, created = CartItem.objects.get_or_create(product=prod, user=request.user)
    return redirect('view_cart')
    
@login_required(login_url='login')
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum([item.product.price * item.quantity for item in cart_items])
    return render(request, 'app/viewcart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, id):
    prod = get_object_or_404(Product, id=id)
    cart_item = get_object_or_404(CartItem, product=prod, user=request.user)
    cart_item.delete()
    return redirect('view_cart')


def increase_quantity(request, id):
    cart_item = get_object_or_404(CartItem, product_id=id, user=request.user)
    if cart_item.quantity < cart_item.product.net_quantity:
        cart_item.quantity += 1
        cart_item.save()
        return redirect('view_cart')
    else:
        messages.error(request, "Item out of stock, please try later.")
        return redirect('view_cart')

def decrease_quantity(request, id):
    cart_item = get_object_or_404(CartItem, product_id=id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('view_cart')

# views.py
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum([item.product.price * item.quantity for item in cart_items])
    return render(request, 'app/checkout.html', {'cart_items': cart_items, 'total': total})



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})




def product_search(request):
    query = request.GET.get('q', '').strip()
    print(f"Search Query: {query}")

    results = Product.objects.filter(title__icontains=query)
    print(f"Results: {results}")

    return render(request, 'app/search_results.html', {'products': results, 'query': query})


@login_required(login_url='login')
def wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)
    return render(request, 'wishlist.html', {'wishlist': wishlist})

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')

def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect('wishlist')


def admin_dashboard(request):
    total_products = Product.objects.count()
    total_customers = User.objects.filter(is_superuser=False).count()  # Exclude superusers/admins
    top_selling_products = top_selling_products_view(request)

    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'top_selling_products': top_selling_products,
    }
    return render(request, 'dashboard.html', context)


import pandas as pd
from django.http import HttpResponse
from .models import Order,OrderItem
from datetime import datetime
import openpyxl  # Ensure openpyxl is imported

import pandas as pd
from django.http import HttpResponse
from datetime import datetime
from .models import Order, OrderItem
import openpyxl 

def sales_report(request):
    # Get all sales data from the Order model
    sales_data = OrderItem.objects.select_related('order', 'product', 'order__user').values(
        'order__id', 'order__user__username', 'product__title', 'quantity', 'order__created_at', 'order__total_price'
    )

    # Convert to a list
    sales_data_list = list(sales_data)

    # Debugging: Print sales data to check if it's being retrieved correctly
    print(f"Sales Data: {sales_data_list}")

    if not sales_data_list:
        return HttpResponse("No sales data available.")

    # Create a DataFrame for exporting
    df = pd.DataFrame(sales_data_list)

    # Rename columns for better clarity
    df.columns = ['Order ID', 'Customer', 'Product', 'Quantity', 'Order Date', 'Total Price']

    # Generate an Excel file response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sales_report.xlsx"'

    # Write the DataFrame to Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response







def top_selling_products_view(request):
    today = timezone.now().date()

    top_selling_products = (
        CartItem.objects
        .filter(product__expiry_date__gte=today)
        .values('product__title')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:10]
    )

    # Prepare data for visualization
    product_titles = [item['product__title'] for item in top_selling_products]
    total_sold = [item['total_sold'] for item in top_selling_products]

    return render(request, 'top_selling_products.html', {
        'product_titles': product_titles,
        'total_sold': total_sold,
    })  

def sales_report_view(request):
    total_sales = OrderItem.objects.aggregate(total=Sum('quantity'))['total'] or 0
    context = {
        'total_sales': total_sales,
    }
    return render(request, 'sales_report.html', context)
  


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import os

# Set your API key
os.environ["GEMINI_API_KEY"] = "AIzaSyA_VjcdSNFywoWL5eDjJnWNbgIyOaBAIOE"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        # Get the user's message from the request
        user_message = request.POST.get('message')

        # Create a chat session
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        "Act as the best hospital and diet recommendation system for the given location.",
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "Please provide me with the location you're interested in!",
                    ],
                },
            ]
        )

        # Send the user's message to the chat session and get a response
        response = chat_session.send_message(user_message)
        
        # Return the response as JSON
        return JsonResponse({'response': response.text})

    return JsonResponse({'error': 'Method not allowed'}, status=405)  # Handle non-POST requests






from django.http import HttpResponse
import pandas as pd
from .models import ProductDetail

def export_product_details_to_excel(request):
    # Fetch product details
    product_details = ProductDetail.objects.all().values('product__title', 'quantity', 'total_price')

    # Check if there are any product details
    if not product_details:
        # Handle the case where there are no product details
        return HttpResponse("No product details available to export.", status=404)

    # Create a DataFrame
    df = pd.DataFrame(product_details)

    # Rename columns for better readability
    df.columns = ['Product Title', 'Quantity', 'Total Price']

    # Create an Excel response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=product_details.xlsx'

    # Write the DataFrame to the Excel file
    df.to_excel(response, index=False)

    return response



from django.shortcuts import render
from django.db.models import Sum
from .models import Order

def sales_by_date(request):
    # Aggregate sales totals by date
    sales_data = Order.objects.values('created_at__date').annotate(total_sales=Sum('total_price')).order_by('created_at__date')

    # Extract dates and sales totals
    sales_dates = [entry['created_at__date'].strftime('%Y-%m-%d') for entry in sales_data]
    total_sales = [entry['total_sales'] for entry in sales_data]

    # Pass the data to the template
    context = {
        'sales_dates': sales_dates,
        'total_sales': total_sales,
    }

    return render(request, 'sales_by_date.html', context)




#def sales_report(request):
    # Get all sales data (Bookings)
    sales_data = Booking.objects.all().values(
        'booking_id', 'user__username', 'total', 'book_date'
    )

    # Convert to a list
    sales_data_list = list(sales_data)

    # Log the sales data for debugging
    print(f"Sales Data: {sales_data_list}")  # Debugging line

    if not sales_data_list:
        return HttpResponse("No sales data available.")

    # Convert datetime fields to timezone-unaware
    for record in sales_data_list:  # {{ edit_1 }}
        if isinstance(record['book_date'], datetime) and record['book_date'].tzinfo is not None:
            record['book_date'] = record['book_date'].replace(tzinfo=None)

    # Create a DataFrame
    df = pd.DataFrame(sales_data_list)

    # Check if DataFrame is empty
    if df.empty:  # {{ edit_2 }}
        return HttpResponse("No sales data available after processing.")

    # Rename the columns for better understanding
    df.columns = ['Booking ID', 'Customer', 'Total Amount', 'Booking Date']
    
    # Create an HTTP response with Excel content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sales_report.xlsx"'
    
    # Write the DataFrame to the response using Excel writer
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response

from django.http import HttpResponse
import pandas as pd
from .models import Product
from datetime import date

def inventory_report(request):
    # Get all products
    products = Product.objects.all()
    
    # Prepare data for the report
    report_data = []
    low_stock_threshold = 10  # Example threshold for low stock

    for product in products:
        # Check for expired products
        is_expired = product.expiry_date < date.today()
        
        # Add product information to report
        report_data.append({
            'Title': product.title,
            'Availability Status': product.availability_status,
            'Current Stock Level': product.net_quantity,
            #'Expiry Date': product.expiry_date,
            'Is Expired': 'Yes' if is_expired else 'No',
            'Low Stock Alert': 'Yes' if product.net_quantity < low_stock_threshold else 'No',
        })

    # Create a DataFrame
    df = pd.DataFrame(report_data)

    # Create an HTTP response with Excel content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.xlsx"'
    
    # Write the DataFrame to the response using Excel writer
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response



