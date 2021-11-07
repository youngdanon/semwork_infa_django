from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include('loginpage.urls')),
    path('pricing', include('shoppage.urls')),
    # path("login", include(''), name="login"),
]
