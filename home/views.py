from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.utils import timezone

from .models import Contact, Service, Booking
from .forms import RegisterForm, BookingForm

from .forms import RegisterForm, BookingForm


# Home Page
def index(request):
    services = Service.objects.all()
    return render(request, 'index.html', {'services': services})


def about(request):
    return render(request, 'about.html')


def services_view(request):
    services = Service.objects.all()
    return render(request, "services.html", {"services": services})


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'home/service_detail.html', {'service': service})


@login_required
def book_service(request):
    service_name = request.GET.get('service')
    service = get_object_or_404(Service, name=service_name)
    success = False
    booked_service = None

    if request.method == 'POST':
        full_name = request.POST.get('full_name', 'Unknown')
        phone = request.POST.get('phone', '0000000000')
        address = request.POST.get('address', 'Not Provided')
        preferred_datetime_str = request.POST.get('preferred_datetime')

        try:
            preferred_datetime = timezone.datetime.fromisoformat(preferred_datetime_str)
        except ValueError:
            preferred_datetime = timezone.now()

        # Create booking
        booking = Booking.objects.create(
            full_name=full_name,
            phone=phone,
            address=address,
            service=service,
            preferred_datetime=preferred_datetime,
            status = "Pending"
        )
        booking.save()
        success = True
        booked_service = service.name

    # Get booking history for the logged-in user (matching full name)
    booking_history = Booking.objects.filter(full_name=request.user.get_full_name()).order_by('-booked_at')

    return render(request, 'book_service.html', {
        'service': service,
        'success': success,
        'booked_service': booked_service,
        'booking_history': booking_history
    })


@staff_member_required
def admin_bookings(request):
    bookings = Booking.objects.all().order_by('-booked_at')
    return render(request, 'admin_bookings.html', {'bookings': bookings})


# Contact Page
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        contact = Contact(
            name=name,
            email=email,
            phone=phone,
            desc=message,
            date=datetime.today()
        )
        contact.save()
        messages.success(request, 'Your message has been sent!')

    return render(request,'contact.html')


# Authentication
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html', {'username_entered': username})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def services(request):
    services = Service.objects.all()
    return render(request, "services.html", {"services": services})


#-------- See the Histroy ---------

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'my_bookings.html', {'bookings': bookings})


@login_required
def update_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status in ["Cancelled", "Completed"]:
        messages.error(request, "You cannot update this booking.")
        return redirect('my_bookings')

    if request.method == "POST":
        preferred_datetime_str = request.POST.get("preferred_datetime")
        try:
            booking.preferred_datetime = timezone.datetime.fromisoformat(preferred_datetime_str)
        except Exception:
            booking.preferred_datetime = timezone.now()

        booking.status = "Pending"  # reset back to pending after reschedule
        booking.save()
        messages.success(request, "Booking updated successfully!")
        return redirect('my_bookings')

    return render(request, 'update_booking.html', {'booking': booking})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status in ["Cancelled", "Completed"]:
        messages.error(request, "This booking cannot be cancelled.")
    else:
        booking.status = "Cancelled"
        booking.save()
        messages.success(request, "Booking cancelled successfully!")

    return redirect('my_bookings')


def booking_states(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')

    # Handle update of preferred datetime
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        new_datetime = request.POST.get("preferred_datetime")
        action = request.POST.get("action")

        booking = get_object_or_404(Booking, id=booking_id, user=request.user)

        if action == "update_datetime":
            booking.preferred_datetime = new_datetime or booking.preferred_datetime
            booking.save()
        elif action == "cancel":
            booking.status = "cancelled"
            booking.save()

        return redirect("booking_states")

    return render(request, "home/booking_states.html", {"bookings": bookings})


def booking_status(request):
    bookings = Booking.objects.filter(user=request.user) if request.user.is_authenticated else None
    return render(request, 'home/booking_status.html', {'bookings': bookings})
    
