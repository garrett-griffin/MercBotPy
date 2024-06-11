from django.urls import path
from dashboard.frontend import views

urlpatterns = [
    path('', views.index, name='index'),
]