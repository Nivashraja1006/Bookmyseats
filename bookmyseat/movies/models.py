from django.db import models
from django.utils import timezone


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    RATING_CHOICES = [
        ('U', 'U - Universal'),
        ('UA', 'UA - Universal Adult'),
        ('A', 'A - Adults Only'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    languages = models.ManyToManyField(Language, related_name='movies')
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    release_date = models.DateField()
    rating = models.CharField(max_length=5, choices=RATING_CHOICES, default='UA')
    imdb_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    poster_url = models.URLField(max_length=500, blank=True, null=True, help_text='Remote poster image URL')
    banner = models.ImageField(upload_to='banners/', blank=True, null=True)
    trailer_youtube_id = models.CharField(max_length=50, blank=True, help_text='YouTube video ID only')
    trailer_url = models.URLField(blank=True, null=True, help_text='Full trailer URL (YouTube watch or embed URL)')
    song_teaser_youtube_id = models.CharField(max_length=20, blank=True, help_text='Fallback teaser video ID')
    is_now_showing = models.BooleanField(default=True)
    is_coming_soon = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return self.title

    def duration_display(self):
        h = self.duration // 60
        m = self.duration % 60
        return f"{h}h {m}m" if h else f"{m}m"

    def get_poster_url(self):
        # Prefer uploaded ImageField
        if self.poster:
            return self.poster.url
        # Then prefer an explicit remote poster URL
        if self.poster_url:
            return self.poster_url
        # Then fall back to a YouTube thumbnail if we have a trailer id
        video_id = self.trailer_youtube_id or self.song_teaser_youtube_id or self.get_trailer_video_id()
        if video_id:
            return f'https://img.youtube.com/vi/{video_id}/hqdefault.jpg'
        return '/static/images/default_poster.jpg'

    def get_trailer_video_id(self):
        # Prefer explicit trailer_url if provided and extract YouTube video id
        if self.trailer_url:
            # Handle typical YouTube URLs (watch?v=ID or youtu.be/ID or embed/ID)
            import re
            m = re.search(r'(?:v=|be/|embed/)([A-Za-z0-9_\-]{6,})', self.trailer_url)
            if m:
                return m.group(1)
        return self.trailer_youtube_id or self.song_teaser_youtube_id

    def get_trailer_embed_url(self):
        # If a full embed URL was provided, use it directly
        if self.trailer_url and '/embed/' in self.trailer_url:
            return self.trailer_url

        video_id = self.get_trailer_video_id()
        if video_id:
            # Use standard YouTube embed domain and enable JS API for better compatibility
            return f'https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1&showinfo=0&enablejsapi=1'
        return ''

    def get_trailer_watch_url(self):
        # If full watch/embed URL provided, normalize to watch URL
        if self.trailer_url and 'youtube' in self.trailer_url:
            # If it's already a watch URL, return it; if embed URL, convert
            if 'watch?v=' in self.trailer_url:
                return self.trailer_url
            # extract id and return watch link
            vid = self.get_trailer_video_id()
            if vid:
                return f'https://www.youtube.com/watch?v={vid}'
        video_id = self.get_trailer_video_id()
        if video_id:
            return f'https://www.youtube.com/watch?v={video_id}'
        return ''


class Theater(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    total_seats = models.PositiveIntegerField(default=100)
    amenities = models.CharField(max_length=300, blank=True, help_text='Comma separated: Dolby, IMAX, etc.')

    def __str__(self):
        return f"{self.name} - {self.city}"


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='shows')
    show_time = models.DateTimeField()
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    price_regular = models.DecimalField(max_digits=8, decimal_places=2, default=150.00)
    price_premium = models.DecimalField(max_digits=8, decimal_places=2, default=250.00)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['show_time']

    def __str__(self):
        return f"{self.movie.title} @ {self.theater.name} - {self.show_time.strftime('%d %b %Y %I:%M %p')}"

    def available_seats_count(self):
        booked = self.seats.filter(is_booked=True).count()
        return self.theater.total_seats - booked


class Seat(models.Model):
    SEAT_TYPES = [
        ('regular', 'Regular'),
        ('premium', 'Premium'),
        ('recliner', 'Recliner'),
    ]
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPES, default='regular')
    is_booked = models.BooleanField(default=False)
    is_held = models.BooleanField(default=False)
    held_until = models.DateTimeField(null=True, blank=True)
    held_by_session = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ('show', 'seat_number')

    def __str__(self):
        return f"{self.seat_number} - {self.show}"

    def is_available(self):
        if self.is_booked:
            return False
        if self.is_held and self.held_until and self.held_until > timezone.now():
            return False
        return True

    def release_if_expired(self):
        if self.is_held and self.held_until and self.held_until <= timezone.now():
            self.is_held = False
            self.held_until = None
            self.held_by_session = ''
            self.save()
            return True
        return False
