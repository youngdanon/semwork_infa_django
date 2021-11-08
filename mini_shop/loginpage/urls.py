from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('changepass', views.change_password, name='change_password')
]
