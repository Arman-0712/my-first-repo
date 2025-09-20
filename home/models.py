from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=15)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=100, blank=True, null=True)  # e.g. "30 mins"
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to="services/", blank=True, null=True)

    def __str__(self):
        return self.name

from django.contrib.auth.models import User

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    full_name = models.CharField(max_length=200, default="Unknown")
    phone = models.CharField(max_length=15, default="0000000000")
    address = models.TextField(default="Not Provided")
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    preferred_datetime = models.DateTimeField(default=timezone.now)
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.full_name} - {self.service.name} ({self.status})"
