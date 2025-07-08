from django.shortcuts import render, redirect
from django.contrib import messages

def checkout_view(request):
    """Vista de checkout/finalizar compra"""
    context = {
        'page_title': 'Finalizar Compra'
    }
    return render(request, 'checkout/checkout.html', context)

def checkout_success(request):
    """Vista de confirmación de compra exitosa"""
    context = {
        'page_title': 'Compra Exitosa',
        'order_number': '12345'
    }
    return render(request, 'checkout/success.html', context)
