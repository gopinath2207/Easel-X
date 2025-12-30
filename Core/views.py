from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from artist.models import Product
from .models import Order
import math, random
from django.contrib.auth import user_logged_in
# from artist.models import Artist
# from Authentication.models import User
# Create your views here.

@login_required(login_url='/')  # Redirect to login if not authenticated
@never_cache
def index(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        return render(request, "index.html", {"user": request.user, "products": products})

    return render(request, "index.html", {"products": products})

@login_required(login_url='/')
@never_cache
def single_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)
    print(product.artist.user.id)
    print(request.user.id)
    print(product.image.url)

    return render(request, "single_pro.html", {"product": product})

@login_required(login_url='/')
@never_cache
def buy_now(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)
    
    random_number = math.floor(random.random() * 10)
    print("Generated Random Number:", random_number)
    if product.quantity <= 0:
        random_number=2
        return render(request, 'order_summary.html', {"number": random_number, "product_id": product.id})
    if(random_number != 2):
        random_number=1
    else:
        return redirect('core:orderFailed_summary', number=random_number)
    if request.method == "POST":
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        email = request.POST.get("email")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postal_code = request.POST.get("postal_code")
        country = request.POST.get("country")
        card_no = request.POST.get("card_no")
        card_expiry = request.POST.get("card_expiry")
        card_cvv = request.POST.get("card_cvv")
        card_holder = request.POST.get("card_holder")
        tax = float(product.price) - 0.82*float(product.price)
        
        order_details = Order(
            firstName=firstName,
            lastName=lastName,
            user=request.user,
            artist=product.artist,
            product=product,
            # total_amount=product.price,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            card_no=card_no,
            card_expiry=card_expiry,
            card_cvv=card_cvv,
            card_holder=card_holder,
            tax=tax,
            total_amount = float(product.price) + tax
        )
        if(random_number==1):
            product.quantity -= 1
            product.save()
            order_details.save()
        # return HttpResponse('payment_success ordersaved')
        print("Order Saved with ID:", order_details.id)
        return redirect('core:order_summary', number=random_number, orders_id=order_details.id)
    # print(type(tax))
    tax = float(product.price) - 0.82*float(product.price)
    total = float(product.price) + tax
    print("Random Number:", random_number)

    return render(request, "buy_now.html", {"product": product, "tax":tax, "total": total})

@login_required(login_url='/')
@never_cache
def order_summary(request, number, orders_id):
    order = Order.objects.get(id=orders_id)
    if(order.user != request.user):
        return HttpResponse("You do not have permission to view this order summary.", status=403)
    if number == 1:
        orders = Order.objects.get(id=orders_id)
        try:
            orders = Order.objects.get(id=orders_id)
        except Order.DoesNotExist:
            return HttpResponse("Order not found", status=404)
        try:
            return render(request, "order_summary.html", {"number": number, "orders": orders})
        except Exception as e:
            return HttpResponse("Error rendering order summary", status=500)
    else:
        return HttpResponse("Page not found", status=404)

@login_required(login_url='/')
@never_cache
def order_Failed_summary(request, number):
    if number == 2:
        return redirect('core:orderFailed_summary', number=number)
    else:
        return redirect('core:index')
    # return HttpResponse("Page not found", status=404)


@login_required(login_url='/')
@never_cache
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return HttpResponse("Order not found or you do not have permission to cancel this order.", status=404)
    
    if order.status != 'CANCELLED':
        order.product.quantity += 1
        order.product.save()
        order.status = 'CANCELLED'
        order.save()
        return redirect("customer:user_dashboard", user_id=request.user.id)
    else:
        return HttpResponse("Order is already cancelled.")