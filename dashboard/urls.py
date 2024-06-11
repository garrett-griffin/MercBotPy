from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.frontend.urls')),  # Assuming 'dashboard.frontend.urls' is a valid URL configuration
]