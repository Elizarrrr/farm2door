# Farm2Door 🌾

A web platform connecting local farmers directly with customers for fresh, affordable produce.

## About

Farm2Door eliminates middlemen by providing farmers with a digital platform to sell their products while giving customers easy access to fresh, healthy food. This project supports UN Sustainable Development Goals: Zero Hunger (SDG 2) and Decent Work and Economic Growth (SDG 8).

## Features

**For Farmers:**

- Register and create an account
- Add, edit, and delete products
- Upload product images
- Set prices and manage stock
- View and manage customer orders
- Track order status

**For Customers:**

- Browse all available products
- Search and filter by category
- View detailed product information
- Place orders with delivery details
- No account required to shop

## Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap 5
- **Database:** SQLite
- **Image Handling:** Pillow

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Farm2Door.git
cd Farm2Door
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install django pillow
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create admin account**
```bash
python manage.py createsuperuser
```

6. **Start the server**
```bash
python manage.py runserver
```

7. **Open your browser**
```
http://127.0.0.1:8000/
```

## Usage

### As a Farmer:

1. Register at `/signup/`
2. Login with your credentials
3. Add products from your dashboard
4. Manage orders as they come in

### As a Customer:

1. Visit the home page
2. Browse or search for products
3. Click "Order Now" on any product
4. Fill in your delivery details
5. Submit your order

### Admin Panel:

Access at `/admin/` with your superuser credentials to manage all users, products, and orders.

## Project Structure

```
Farm2Door/
├── core/                 # Main app
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── forms.py         # Form definitions
│   └── urls.py          # URL routes
├── templates/           # HTML templates
├── media/              # Uploaded images
├── farm2door/          # Project settings
└── manage.py           # Django management script
```

## Acknowledgments

- Supports local farmers and food security
- Aligned with UN Sustainable Development Goals

---

**Live Demo:** [https://farm2door-7ik3.onrender.com](https://farm2door-7ik3.onrender.com)
