from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from movies.models import Seat


def generate_seats_for_show(show):
    """Auto-generate seats for a show based on theater capacity."""
    total = show.theater.total_seats
    rows = 'ABCDEFGHIJKLMNOPQRST'
    seats_per_row = 10
    num_rows = (total + seats_per_row - 1) // seats_per_row

    # Last 2 rows = premium
    premium_rows = max(2, num_rows // 4)

    seats_to_create = []
    count = 0
    for i in range(num_rows):
        if count >= total:
            break
        row = rows[i] if i < len(rows) else f'R{i}'
        seat_type = 'premium' if i >= (num_rows - premium_rows) else 'regular'
        for j in range(1, seats_per_row + 1):
            if count >= total:
                break
            seats_to_create.append(Seat(
                show=show,
                seat_number=f"{row}{j}",
                seat_type=seat_type,
                is_booked=False,
                is_held=False
            ))
            count += 1

    Seat.objects.bulk_create(seats_to_create, ignore_conflicts=True)


def send_booking_confirmation_email(booking):
    """Send booking confirmation email to user."""
    subject = f"BookMySeat - Booking Confirmed! [{booking.booking_id}]"

    html_message = render_to_string('bookings/email_confirmation.html', {
        'booking': booking,
        'user': booking.user,
        'show': booking.show,
        'movie': booking.show.movie,
        'theater': booking.show.theater,
        'seats': booking.seats.all(),
    })

    plain_message = f"""
Booking Confirmed!

Booking ID: {booking.booking_id}
Movie: {booking.show.movie.title}
Theater: {booking.show.theater.name}, {booking.show.theater.city}
Show Time: {booking.show.show_time.strftime('%d %b %Y, %I:%M %p')}
Seats: {booking.seat_numbers()}
Total Amount: ₹{booking.total_amount}

Thank you for booking with BookMySeat!
"""

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.user.email],
        html_message=html_message,
        fail_silently=False,
    )
