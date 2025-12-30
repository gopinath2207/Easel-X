from django.urls import path
from . import views

# Do NOT import Core.views here; it would shadow the local `views` module.
# If you need Core views in this file, import them with an alias, e.g.
# from Core import views as core_views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
]