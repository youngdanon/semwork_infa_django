from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.get_users_list, name='adminpanel'),
    path('user/<slug:username>', views.user_info_request, name='user_info'),
    path('products', views.display_products_request, name='products'),
    path('product/<int:product_id>', views.display_product_info_request, name='product_card'),
    path('products/add', views.add_product_request, name='add_product'),
    path('products/delete/<int:product_id>', views.delete_product_request, name='delete_product')
]
