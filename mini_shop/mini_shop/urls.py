from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('main.urls')),
    path('accounts/', include('loginpage.urls')),
    path('pricing', include('shoppage.urls')),
    # path("login", include(''), name="login"),
    path('admin/', include('adminpanel.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
