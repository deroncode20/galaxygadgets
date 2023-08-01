

from django.shortcuts import render, get_object_or_404
from .models import Product  # Replace 'your_app' with the actual name of your app

from django.shortcuts import render
from .models import Product, Category
from django.core.paginator import Paginator

def single_product(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug, is_available=True)

    # Get related products (products from the same category, excluding the current product)
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]

    return render(request, 'stock/single_product.html', {'product': product, 'related_products': related_products})


def store(request, category_slug=None):
    categories = Category.objects.all()
    products_per_page = 4
    page_number = request.GET.get('page')

    if category_slug:
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        product_count = products.count()

    paginator = Paginator(products, products_per_page)
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'category': category if category_slug else None,
        'categories': categories,
        'product_count': product_count,
    }

    return render(request, 'stock/store.html', context)
