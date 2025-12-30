from django.urls import path
from . import views

# Provide an application namespace so reverse('core:index') works.
app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/', views.single_product, name='single_product'),
    path('buy/<int:product_id>/', views.buy_now, name='buy_now'),
    path('order-summary/<int:number>/<int:orders_id>/', views.order_summary, name='order_summary'),
    path('order-summary/<int:number>/', views.order_Failed_summary, name='orderFailed_summary'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
]
