from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from movies.models import Show, Seat
from .models import Booking
from .utils import send_booking_confirmation_email, generate_seats_for_show
import razorpay
import json
import hmac
import hashlib


def get_or_create_seats(show):
    """Auto-create seats for a show if they don't exist."""
    if not show.seats.exists():
        generate_seats_for_show(show)


@login_required
def seat_selection_view(request, show_id):
    show = get_object_or_404(Show, id=show_id, is_active=True)
    get_or_create_seats(show)

    # Release expired holds
    expired = show.seats.filter(is_held=True, held_until__lte=timezone.now())
    expired.update(is_held=False, held_until=None, held_by_session='')

    seats = show.seats.all().order_by('seat_number')

    # Organize seats into rows
    rows = {}
    for seat in seats:
        row = seat.seat_number[0]
        if row not in rows:
            rows[row] = []
        rows[row].append(seat)

    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    held_by_me = show.seats.filter(is_held=True, held_by_session=session_key).values_list('seat_number', flat=True)

    return render(request, 'bookings/seat_selection.html', {
        'show': show,
        'rows': rows,
        'held_by_me': list(held_by_me),
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    })


@login_required
@require_POST
def hold_seats_view(request):
    """Hold seats for 5 minutes."""
    data = json.loads(request.body)
    seat_numbers = data.get('seats', [])
    show_id = data.get('show_id')

    if not seat_numbers or not show_id:
        return JsonResponse({'success': False, 'error': 'Invalid data'})

    if len(seat_numbers) > 10:
        return JsonResponse({'success': False, 'error': 'Max 10 seats at a time'})

    show = get_object_or_404(Show, id=show_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    # Release previous holds by this session
    show.seats.filter(is_held=True, held_by_session=session_key).update(
        is_held=False, held_until=None, held_by_session=''
    )

    # Release expired holds
    show.seats.filter(is_held=True, held_until__lte=timezone.now()).update(
        is_held=False, held_until=None, held_by_session=''
    )

    # Try to hold new seats
    seats = show.seats.filter(seat_number__in=seat_numbers)
    unavailable = []
    for seat in seats:
        if not seat.is_available():
            unavailable.append(seat.seat_number)

    if unavailable:
        return JsonResponse({'success': False, 'error': f'Seats {", ".join(unavailable)} are no longer available'})

    hold_until = timezone.now() + timezone.timedelta(minutes=settings.SEAT_HOLD_MINUTES)
    seats.update(is_held=True, held_until=hold_until, held_by_session=session_key)

    # Calculate total
    total = 0
    for seat in seats:
        if seat.seat_type == 'premium':
            total += float(show.price_premium)
        elif seat.seat_type == 'recliner':
            total += float(show.price_premium) * 1.5
        else:
            total += float(show.price_regular)

    return JsonResponse({
        'success': True,
        'hold_until': hold_until.isoformat(),
        'total': total,
        'seat_count': len(seat_numbers),
    })


@login_required
@require_POST
def create_order_view(request):
    """Create Razorpay order."""
    data = json.loads(request.body)
    show_id = data.get('show_id')
    seat_numbers = data.get('seats', [])

    show = get_object_or_404(Show, id=show_id)
    session_key = request.session.session_key

    seats = show.seats.filter(
        seat_number__in=seat_numbers,
        is_held=True,
        held_by_session=session_key
    )

    if seats.count() != len(seat_numbers):
        return JsonResponse({'success': False, 'error': 'Seat hold expired. Please reselect seats.'})

    # Calculate total
    total = 0
    for seat in seats:
        if seat.seat_type == 'premium':
            total += float(show.price_premium)
        elif seat.seat_type == 'recliner':
            total += float(show.price_premium) * 1.5
        else:
            total += float(show.price_regular)

    amount_paise = int(total * 100)

    # Check if Razorpay keys are configured
    razorpay_key_id = getattr(settings, 'RAZORPAY_KEY_ID', '')
    razorpay_key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
    
    if (not razorpay_key_id or razorpay_key_id.startswith('rzp_test_your') or 
        not razorpay_key_secret or razorpay_key_secret.startswith('your_')):
        return JsonResponse({
            'success': False,
            'error': 'Payment gateway not configured. Please add your Razorpay keys to the .env file. Get free test keys at razorpay.com',
            'configuration_error': True
        })

    try:
        client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))
        order = client.order.create({
            'amount': amount_paise,
            'currency': 'INR',
            'payment_capture': 1,
            'notes': {
                'show_id': str(show_id),
                'user_id': str(request.user.id),
                'seats': ','.join(seat_numbers)
            }
        })

        # Create pending booking
        booking = Booking.objects.create(
            user=request.user,
            show=show,
            total_amount=total,
            status='pending',
            razorpay_order_id=order['id']
        )
        booking.seats.set(seats)

        return JsonResponse({
            'success': True,
            'order_id': order['id'],
            'amount': amount_paise,
            'currency': 'INR',
            'booking_id': booking.id,
            'key': settings.RAZORPAY_KEY_ID,
            'name': request.user.get_full_name() or request.user.email,
            'email': request.user.email,
            'phone': request.user.phone if hasattr(request.user, 'phone') else '',
        })
    except Exception as e:
        error_msg = str(e)
        # Check if it's an authentication error
        if any(auth_error in error_msg.lower() for auth_error in ['unauthorized', '401', 'authentication', 'invalid api key', 'invalid credentials']):
            return JsonResponse({
                'success': False,
                'error': 'Razorpay authentication failed. Please configure your API keys in the .env file.',
                'authentication_error': True
            })
        # Check for connection errors
        if any(conn_error in error_msg.lower() for conn_error in ['connection', 'timeout', 'network', 'refused']):
            return JsonResponse({
                'success': False,
                'error': 'Unable to connect to payment gateway. Please check your internet connection and try again.'
            })
        return JsonResponse({'success': False, 'error': error_msg or 'An error occurred while processing your payment.'})


@login_required
@csrf_exempt
@require_POST
def payment_callback_view(request):
    """Handle Razorpay payment callback."""
    data = json.loads(request.body)
    razorpay_order_id = data.get('razorpay_order_id')
    razorpay_payment_id = data.get('razorpay_payment_id')
    razorpay_signature = data.get('razorpay_signature')
    booking_id = data.get('booking_id')

    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Verify signature
    try:
        key_secret = settings.RAZORPAY_KEY_SECRET.encode('utf-8')
        msg = f"{razorpay_order_id}|{razorpay_payment_id}".encode('utf-8')
        generated_signature = hmac.new(key_secret, msg, hashlib.sha256).hexdigest()

        if generated_signature == razorpay_signature:
            # Payment verified
            booking.status = 'confirmed'
            booking.razorpay_payment_id = razorpay_payment_id
            booking.razorpay_signature = razorpay_signature
            booking.save()

            # Mark seats as booked
            for seat in booking.seats.all():
                seat.is_booked = True
                seat.is_held = False
                seat.held_until = None
                seat.save()

            # Send confirmation email
            try:
                send_booking_confirmation_email(booking)
                booking.email_sent = True
                booking.save()
            except Exception as e:
                pass  # Email failure shouldn't block booking confirmation

            return JsonResponse({'success': True, 'redirect': f'/bookings/confirmation/{booking.booking_id}/'})
        else:
            booking.status = 'failed'
            booking.save()
            return JsonResponse({'success': False, 'error': 'Payment verification failed'})
    except Exception as e:
        booking.status = 'failed'
        booking.save()
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def booking_confirmation_view(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    return render(request, 'bookings/confirmation.html', {'booking': booking})


@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user).prefetch_related(
        'seats', 'show__movie', 'show__theater'
    ).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
@require_POST
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    if booking.status == 'confirmed':
        show_time = booking.show.show_time
        if show_time > timezone.now() + timezone.timedelta(hours=2):
            booking.status = 'cancelled'
            booking.save()
            for seat in booking.seats.all():
                seat.is_booked = False
                seat.save()
            messages.success(request, 'Booking cancelled successfully.')
        else:
            messages.error(request, 'Cannot cancel booking less than 2 hours before show.')
    return redirect('my_bookings')


@login_required
@require_POST
def demo_booking_view(request):
    import json, uuid
    data = json.loads(request.body)
    show = get_object_or_404(Show, id=data.get('show_id'))
    seats = show.seats.filter(seat_number__in=data.get('seats',[]))
    total = sum(float(show.price_premium) if s.seat_type=='premium' else float(show.price_regular) for s in seats)
    booking = Booking.objects.create(user=request.user, show=show, total_amount=total, status='confirmed', razorpay_order_id='DEMO_'+uuid.uuid4().hex[:6].upper(), razorpay_payment_id='PAY_'+uuid.uuid4().hex[:6].upper())
    booking.seats.set(seats)
    seats.update(is_booked=True, is_held=False, held_until=None)
    return JsonResponse({'success':True,'redirect':f'/bookings/confirmation/{booking.booking_id}/'})
