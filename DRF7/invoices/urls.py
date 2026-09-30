from django.urls import include, path 
from . import views

urlpatterns = [
    path('add/', views.add_invoice, name='add_invoice'),
]