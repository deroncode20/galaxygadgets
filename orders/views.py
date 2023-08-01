# views.py

import requests
from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm
from cart.models import CartItem
import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from decouple import config



public_key = config('FLUTTERWAVE_PUBLIC_KEY')


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to the store
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = ((1/2) * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside the Order table
            data = form.save(commit=False)
            data.user = current_user
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # 20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            order_id = data.id
            
            data.save()

            # Redirect to the payment function passing the order_id
            return redirect('payments', order_id=order_id)
    else:
        return redirect('checkout')

    return HttpResponseBadRequest("Invalid request")


def payments(request, order_id):
    # Get the order details from the database based on the order_id
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)

    payload = {
        "public_key": str(public_key),
        "tx_ref": 'FLWSECK_TESTa350fa9dd1fb'+ str(order.order_number),
        "amount": order.order_total,
        "currency": "UGX",  
        'redirect_url': 'http://127.0.0.1:8000/order_complete/',  
        'payment_options': 'card,mobilemoneyuganda',
        'meta': {
            'customer_id': str(request.user.id),
            'order_id': order_id,
        },
        'customer': {
            'email': request.user.email,
            'phonenumber': request.user.phone_number,
            'name': request.user.username,
        },
        'customizations': {
                'title': "The Titanic Store",
                'description': "Payment for an awesome cruise",
                'logo': "https://www.logolynx.com/images/logolynx/22/2239ca38f5505fbfce7e55bbc0604386.jpeg",
        },  
    }

    secret_key =  config('FLUTTERWAVE_SECRET_KEY')
    headers = {
        "Authorization": f'Bearer {secret_key}',
        "Content-Type": "application/json",
    }

    try:
        response = requests.post("https://api.flutterwave.com/v3/payments", json=payload, headers=headers)
        if response.status_code != 200:
            return JsonResponse({"error": f"Request failed with status code {response.status_code}"}, status=500)
        if not response.text:
            return JsonResponse({"error": "Empty response from API"}, status=500)
        data = response.json()

        if data.get("status") == "success":
            payment = Payment.objects.create(
                user=request.user,
                payment_id=data.get("data").get("tx_ref"),
                payment_method=data.get("data").get("payment_type"),
                amount_paid=order.order_total,
                status="success",
            )
            order.payment = payment
            order.save()

            return JsonResponse(data, status=200)
        else:
            return JsonResponse(data, status=400)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

    except ValueError as ve:
        return JsonResponse({"error": "Invalid JSON format in the API response"}, status=500)
