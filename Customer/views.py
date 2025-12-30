from django.shortcuts import render, redirect
from Core.models import Order
from django.http import HttpResponse
# Create your views here.

def user_dashboard(request, user_id):
    user_orders = Order.objects.filter(user_id=user_id)
    pending_orders = user_orders.filter(status ='Pending').count() + user_orders.filter(status ='Processing').count()+ user_orders.filter(status ='Shipping').count()
    total_spent = sum(float(order.total_amount) for order in user_orders) - sum(float(order.total_amount) for order in user_orders if order.status == 'Failed' or order.status == 'CANCELLED')
    context = {
        'orders': user_orders,
        'pending_orders': pending_orders,
        'total_spent': int(total_spent)
    }
    return render(request, "user_dash.html", context)

def order_details(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return HttpResponse("Order not found or you do not have permission to view this order.", status=404)
    number = 2
    context = {
        'order': order
    }
    print(order.id)
    return render(request, "orderdetails.html", context)
