from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Order, FarmerProfile
from .forms import FarmerSignUpForm, ProductForm, OrderForm

# Create your views here.

# Home page - displays all products for customers
def home(request):
    # Get search query if exists
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    # Filter products based on search
    products = Product.objects.all()
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    if category:
        products = products.filter(category=category)
    
    # Get all categories for filter
    categories = Product.CATEGORY_CHOICES
    
    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category,
    }
    return render(request, 'home.html', context)

# Farmer registration view
def farmer_signup(request):
    if request.method == 'POST':
        form = FarmerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Farm2Door.')
            return redirect('farmer_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FarmerSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Farmer login view
def farmer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('farmer_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')

# Farmer logout view
def farmer_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

# Farmer dashboard - shows farmer's products and orders
@login_required
def farmer_dashboard(request):
    # Get all products belonging to this farmer
    products = Product.objects.filter(farmer=request.user)
    
    # Get all orders for this farmer's products
    orders = Order.objects.filter(product__farmer=request.user)
    
    context = {
        'products': products,
        'orders': orders,
    }
    return render(request, 'farmer/dashboard.html', context)

# Add new product
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user  # Set the farmer to current user
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('farmer_dashboard')
    else:
        form = ProductForm()
    
    return render(request, 'farmer/add_product.html', {'form': form})

# Edit existing product
# @login_required
# def edit_product(request, pk):
#     product = get_object_or_404(Product, pk=pk, farmer=request.user)
    
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Product updated successfully!')
#             return redirect('farmer_dashboard')
#     else:
#         form = ProductForm(instance=product)
    
#     return render(request, 'farmer/edit_product.html', {'form': form, 'product': product})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, farmer=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # If a new image is uploaded, delete the old one
            if 'image' in request.FILES:
                # Delete old image file if it exists
                if product.image:
                    import os
                    if os.path.isfile(product.image.path):
                        os.remove(product.image.path)
            
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('farmer_dashboard')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'farmer/edit_product.html', {'form': form, 'product': product})

# Delete product
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, farmer=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('farmer_dashboard')
    
    return render(request, 'farmer/delete_product.html', {'product': product})

# Product detail page for customers
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

# Place order - customer side
def place_order(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            # Calculate total price
            order.total_price = product.price * order.quantity
            
            # Check if enough stock is available
            if order.quantity > product.stock:
                messages.error(request, f'Sorry, only {product.stock} {product.unit} available.')
                return render(request, 'place_order.html', {'form': form, 'product': product})
            
            order.save()
            
            # Reduce stock
            product.stock -= order.quantity
            product.save()
            
            messages.success(request, 'Order placed successfully! The farmer will contact you soon.')
            return redirect('home')
    else:
        form = OrderForm()
    
    return render(request, 'place_order.html', {'form': form, 'product': product})

# Update order status - farmer side
@login_required
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk, product__farmer=request.user)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            messages.success(request, f'Order status updated to {order.get_status_display()}.')
        else:
            messages.error(request, 'Invalid status.')
    
    return redirect('farmer_dashboard')