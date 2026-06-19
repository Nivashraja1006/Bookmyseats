import os
import urllib.request
import urllib.parse
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from movies.models import Movie

TMDB_SEARCH_URL = 'https://api.themoviedb.org/3/search/movie'
TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500'


class Command(BaseCommand):
    help = 'Populate Movie.poster by downloading images from TMDb (if TMDB_API_KEY set) or YouTube thumbnails.'

    def add_arguments(self, parser):
        parser.add_argument('--tmdb-key', dest='tmdb_key', help='TMDb API key (optional)')
        parser.add_argument('--dry-run', action='store_true', help='Do not save files; only report')

    def handle(self, *args, **options):
        tmdb_key = options.get('tmdb_key') or os.environ.get('TMDB_API_KEY')
        dry_run = options.get('dry_run', False)

        qs = Movie.objects.all()
        total = qs.count()
        if total == 0:
            self.stdout.write('No movies found.')
            return

        posters_dir = os.path.join(settings.MEDIA_ROOT, 'posters')
        os.makedirs(posters_dir, exist_ok=True)

        for movie in qs:
            if movie.poster:
                self.stdout.write(f'SKIP {movie.id} {movie.title} (already has poster)')
                continue

            img_url = None

            if tmdb_key:
                # Try TMDb search
                query = urllib.parse.urlencode({'api_key': tmdb_key, 'query': movie.title})
                url = f"{TMDB_SEARCH_URL}?{query}"
                try:
                    with urllib.request.urlopen(url, timeout=10) as resp:
                        import json
                        data = json.loads(resp.read().decode('utf-8'))
                        results = data.get('results') or []
                        if results:
                            poster_path = results[0].get('poster_path')
                            if poster_path:
                                img_url = TMDB_IMAGE_BASE + poster_path
                except Exception as e:
                    self.stdout.write(f'TMDb lookup failed for "{movie.title}": {e}')

            # Fallback to YouTube thumbnail if trailer id exists
            if not img_url:
                vid = movie.get_trailer_video_id()
                if vid:
                    # Try a list of thumbnail variants until one works
                    variants = ['maxresdefault.jpg', 'hqdefault.jpg', 'sddefault.jpg', 'mqdefault.jpg', 'default.jpg']
                    for v in variants:
                        candidate = f'https://img.youtube.com/vi/{vid}/{v}'
                        try:
                            req = urllib.request.Request(candidate, headers={'User-Agent': 'Mozilla/5.0'})
                            with urllib.request.urlopen(req, timeout=10) as resp:
                                # If the request succeeds and content length reasonable, pick this
                                content = resp.read()
                                if len(content) > 100:
                                    img_url = candidate
                                    break
                        except Exception:
                            continue

            if not img_url:
                self.stdout.write(f'NO IMAGE for {movie.id} {movie.title}')
                continue

            try:
                req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    content = resp.read()
                    if len(content) < 100:
                        raise ValueError('Downloaded content too small')

                filename = f'posters/movie_{movie.id}.jpg'
                if dry_run:
                    self.stdout.write(f'DRY {movie.id} {movie.title}: would save {img_url} -> {filename}')
                else:
                    movie.poster.save(filename, ContentFile(content), save=True)
                    self.stdout.write(f'SAVED {movie.id} {movie.title}: {filename}')
            except Exception as e:
                self.stdout.write(f'FAILED {movie.id} {movie.title}: {e}')

        self.stdout.write('Done')
