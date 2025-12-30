from django.urls import path
from . import views

app_name = 'artist'

urlpatterns = [
    path('', views.artist_dashboard, name='artist_dashboard'),
    path('profile/<int:artist_id>/', views.artist_profile, name='artist_profile'),
    path('create_profile/', views.create_artist_profile, name='create_artist_profile'),
    path('edit_profile/<int:artist_id>/', views.edit_profile, name='edit_artist_profile'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

]