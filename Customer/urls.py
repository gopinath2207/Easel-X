from django.urls import path
from . import views
from Core.models import Order

app_name = 'customer'

urlpatterns = [
    path('dashboard/<int:user_id>/', views.user_dashboard, name='user_dashboard'),
    path('order/<int:order_id>/', views.order_details, name='order_details'),
    # path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
]