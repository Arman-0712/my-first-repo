from django.contrib import admin
from django.urls import path
from home import views  # to pass the data into the views
from .models import Service, Booking

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('contact', views.contact, name='contact'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('book-service/', views.book_service, name='book_service'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),  # ✅ added comma
    path('services/', views.services_view, name='services_view'),
]
