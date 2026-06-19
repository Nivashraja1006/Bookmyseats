from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from bookings.models import Booking
from movies.models import Movie, Show, Theater
from users.models import CustomUser
import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


@staff_member_required
def admin_dashboard(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    # Summary stats
    total_bookings = Booking.objects.filter(status='confirmed').count()
    total_revenue = Booking.objects.filter(status='confirmed').aggregate(
        total=Sum('total_amount'))['total'] or 0
    total_users = CustomUser.objects.count()
    total_movies = Movie.objects.filter(is_now_showing=True).count()

    today_bookings = Booking.objects.filter(
        status='confirmed', created_at__date=today
    ).count()
    today_revenue = Booking.objects.filter(
        status='confirmed', created_at__date=today
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    month_revenue = Booking.objects.filter(
        status='confirmed', created_at__date__gte=month_start
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    # Revenue last 30 days
    last_30 = today - timezone.timedelta(days=29)
    daily_revenue = list(Booking.objects.filter(
        status='confirmed', created_at__date__gte=last_30
    ).annotate(date=TruncDate('created_at')).values('date').annotate(
        revenue=Sum('total_amount'), count=Count('id')
    ).order_by('date'))

    # Fill missing days
    revenue_map = {r['date']: {'revenue': float(r['revenue'] or 0), 'count': r['count']} for r in daily_revenue}
    revenue_labels = []
    revenue_data = []
    bookings_data = []
    for i in range(30):
        d = last_30 + timezone.timedelta(days=i)
        revenue_labels.append(d.strftime('%d %b'))
        revenue_data.append(revenue_map.get(d, {}).get('revenue', 0))
        bookings_data.append(revenue_map.get(d, {}).get('count', 0))

    # Top movies by bookings
    top_movies = Booking.objects.filter(status='confirmed').values(
        'show__movie__title'
    ).annotate(count=Count('id'), revenue=Sum('total_amount')).order_by('-count')[:5]

    # Bookings by genre
    genre_stats = Booking.objects.filter(status='confirmed').values(
        'show__movie__genres__name'
    ).annotate(count=Count('id')).order_by('-count')[:6]
    genre_labels = [g['show__movie__genres__name'] or 'Other' for g in genre_stats]
    genre_data = [g['count'] for g in genre_stats]

    # Recent bookings
    recent_bookings = Booking.objects.filter(status='confirmed').select_related(
        'user', 'show__movie', 'show__theater'
    ).order_by('-created_at')[:10]

    context = {
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'total_users': total_users,
        'total_movies': total_movies,
        'today_bookings': today_bookings,
        'today_revenue': today_revenue,
        'month_revenue': month_revenue,
        'recent_bookings': recent_bookings,
        'top_movies': top_movies,
        'revenue_labels': json.dumps(revenue_labels),
        'revenue_data': json.dumps(revenue_data),
        'bookings_data': json.dumps(bookings_data),
        'genre_labels': json.dumps(genre_labels),
        'genre_data': json.dumps(genre_data),
    }
    return render(request, 'admin_dashboard/dashboard.html', context)
