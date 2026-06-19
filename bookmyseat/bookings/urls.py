from django.urls import path
from . import views

urlpatterns = [
    path('select-seats/<int:show_id>/', views.seat_selection_view, name='seat_selection'),
    path('hold-seats/', views.hold_seats_view, name='hold_seats'),
    path('create-order/', views.create_order_view, name='create_order'),
    path('payment-callback/', views.payment_callback_view, name='payment_callback'),
    path('confirmation/<str:booking_id>/', views.booking_confirmation_view, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('cancel/<str:booking_id>/', views.cancel_booking_view, name='cancel_booking'),
    path('demo-booking/', views.demo_booking_view, name='demo_booking'),
]
