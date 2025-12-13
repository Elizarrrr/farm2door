from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/order/', views.place_order, name='place_order'),
    
    # Authentication
    path('signup/', views.farmer_signup, name='signup'),
    path('login/', views.farmer_login, name='login'),
    path('logout/', views.farmer_logout, name='logout'),
    
    # Farmer dashboard
    path('dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('order/<int:pk>/update-status/', views.update_order_status, name='update_order_status'),
]