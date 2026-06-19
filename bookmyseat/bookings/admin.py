from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'show', 'total_amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('booking_id', 'user__email')
    readonly_fields = ('booking_id', 'created_at', 'updated_at')
