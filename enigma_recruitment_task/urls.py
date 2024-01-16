from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("enigma_ecommerce/", include("enigma_ecommerce.urls")),
    path('admin/', admin.site.urls),
]