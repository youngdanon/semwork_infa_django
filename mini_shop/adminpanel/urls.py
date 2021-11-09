from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.get_users_list, name='adminpanel'),
    path('user/<slug:username>', views.user_info_request, name='user_info')
]
