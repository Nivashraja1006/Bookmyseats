from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Movie, Genre, Language, Show, Theater
from django.utils import timezone


def home_view(request):
    now_showing = Movie.objects.filter(is_now_showing=True).prefetch_related('genres', 'languages')[:8]
    coming_soon = Movie.objects.filter(is_coming_soon=True).prefetch_related('genres')[:4]
    genres = Genre.objects.all()
    languages = Language.objects.all()
    return render(request, 'movies/home.html', {
        'now_showing': now_showing,
        'coming_soon': coming_soon,
        'genres': genres,
        'languages': languages,
    })


def movie_list_view(request):
    movies = Movie.objects.filter(is_now_showing=True).prefetch_related('genres', 'languages')
    genres = Genre.objects.all()
    languages = Language.objects.all()

    # Filters
    genre_id = request.GET.get('genre')
    language_id = request.GET.get('language')
    search = request.GET.get('search', '').strip()

    if genre_id:
        movies = movies.filter(genres__id=genre_id)
    if language_id:
        movies = movies.filter(languages__id=language_id)
    if search:
        movies = movies.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )

    movies = movies.distinct()

    selected_genre = Genre.objects.filter(id=genre_id).first() if genre_id else None
    selected_language = Language.objects.filter(id=language_id).first() if language_id else None

    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'genres': genres,
        'languages': languages,
        'selected_genre': selected_genre,
        'selected_language': selected_language,
        'search': search,
    })


def movie_detail_view(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    # Use timezone-aware datetime filtering to avoid missing shows
    # because of date vs timezone mismatches. Show upcoming shows
    # from now up to the next 7 days.
    now = timezone.now()
    end = now + timezone.timedelta(days=7)
    shows = Show.objects.filter(
        movie=movie,
        show_time__gte=now,
        show_time__lte=end,
        is_active=True
    ).select_related('theater', 'language').order_by('show_time')

    # Group shows by date
    shows_by_date = {}
    for show in shows:
        date = show.show_time.date()
        if date not in shows_by_date:
            shows_by_date[date] = []
        shows_by_date[date].append(show)

    # Build a date range starting today for the next 7 days
    today = now.date()
    date_range = [today + timezone.timedelta(days=i) for i in range(7)]

    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'shows_by_date': shows_by_date,
        'date_range': date_range,
        'today': today,
    })
