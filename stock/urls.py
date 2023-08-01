# urls.py

from django.urls import path
from .views import *  # Replace 'your_app' with the actual name of your app

urlpatterns = [
    # Your other URL patterns...
    path('category/<slug:category_slug>/<slug:product_slug>/', single_product, name='product_detail'),
     path('accessories/<slug:category_slug>/', store, name='products_by_category'),
     path('accessories/', store , name='store'),
]
