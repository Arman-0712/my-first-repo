from django.contrib import admin
from home.models import Contact     #to take the database name of the models 
from .models import Service, Booking #to take a service database name 


# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "description")
    search_fields = ("name",)


admin.site.register(Contact)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'service', 'preferred_datetime', 'status', 'booked_at')
    list_filter = ('status', 'service', 'preferred_datetime')
    search_fields = ('full_name', 'phone', 'address')
    list_editable = ('status',)  # admin can change status directly in list view

admin.site.register(Booking, BookingAdmin)
