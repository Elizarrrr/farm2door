from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Order, FarmerProfile

# Form for farmer registration
class FarmerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    location = forms.CharField(max_length=200, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'location', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create farmer profile
            FarmerProfile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone', ''),
                location=self.cleaned_data.get('location', '')
            )
        return user

# Form for adding/editing products
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'unit', 'description', 'stock', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Fresh Tomatoes'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 50.00'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., kg, dozen, liters'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your product...'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Available quantity'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

# Form for customer orders
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'customer_email', 'delivery_location', 'quantity', 'notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., +254712345678'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}),
            'delivery_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full delivery address'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'value': 1}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special instructions? (Optional)'}),
        }