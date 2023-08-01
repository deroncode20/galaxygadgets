from .models import Category
from stock.models import  *
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)

def popular_products(request):
    products =Product.objects.all()[:5]

    context= {
        'products':products
    }
    return context
# context_processors.py


  # Replace 'your_app' with the actual name of your app

""" def all_products(request, category_slug=None):
    categories = None
    products = None
    products_per_page = 4
    page_number = request.GET.get('page')

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        product_count = products.count()

    paginator = Paginator(products, products_per_page)
    page_obj = paginator.get_page(page_number)
    context = {'products': page_obj, 'category': categories,'product_count': product_count,}

    return context """

