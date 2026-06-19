from django.contrib import admin
from .models import Genre, Language, Movie, Theater, Show, Seat


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'release_date', 'is_now_showing', 'is_coming_soon')
    list_filter = ('is_now_showing', 'is_coming_soon', 'genres')
    filter_horizontal = ('genres', 'languages')
    search_fields = ('title',)


@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'location', 'total_seats')


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theater', 'show_time', 'language', 'is_active')
    list_filter = ('is_active', 'theater')
    search_fields = ('movie__title',)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'show', 'seat_type', 'is_booked', 'is_held')
    list_filter = ('seat_type', 'is_booked')
