from django.urls import path
from . import views

urlpatterns = [
    path('', views.pricing, name='pricing'),
    path('product/<int:id>', views.product_card_request, name='product_card')
]