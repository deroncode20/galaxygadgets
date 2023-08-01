# context_processors.py

from .models import Product  # Replace 'your_app' with the actual name of your app

def products_with_sell_price(request):
    products_with_sell_price = Product.objects.filter(sell_price__gt=0, is_available=True)
    context = {
        'products_with_sell_price': products_with_sell_price
        }
    return context

def latest_products(request):
    latest_products = Product.objects.filter(is_available=True).order_by('-created_date')[:5]
    return {'latest_products': latest_products}

