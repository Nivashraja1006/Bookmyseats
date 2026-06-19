from django.core.management.base import BaseCommand
from django.utils import timezone
from movies.models import Genre, Language, Movie, Theater, Show
from users.models import CustomUser
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Seed the database with sample movies, theaters, and shows'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding database...')

        # Genres
        genres_data = ['Action', 'Drama', 'Comedy', 'Horror', 'Romance', 'Sci-Fi', 'Thriller', 'Animation']
        genres = {}
        for g in genres_data:
            obj, _ = Genre.objects.get_or_create(name=g)
            genres[g] = obj
        self.stdout.write('  ✓ Genres created')

        # Languages
        languages_data = ['Hindi', 'English', 'Tamil', 'Telugu', 'Malayalam', 'Kannada']
        languages = {}
        for l in languages_data:
            obj, _ = Language.objects.get_or_create(name=l)
            languages[l] = obj
        self.stdout.write('  ✓ Languages created')

        # Theaters
        theaters_data = [
            {'name': 'PVR Cinemas', 'location': 'Phoenix Mall, Nungambakkam', 'city': 'Chennai', 'total_seats': 120, 'amenities': 'Dolby Atmos, 4K'},
            {'name': 'INOX Multiplex', 'location': 'Forum Mall, Koramangala', 'city': 'Bangalore', 'total_seats': 100, 'amenities': 'IMAX, Dolby'},
            {'name': 'Cinepolis', 'location': 'Brookefields Mall, Whitefield', 'city': 'Bangalore', 'total_seats': 90, 'amenities': 'Dolby Atmos'},
            {'name': 'Sathyam Cinemas', 'location': 'Royapettah', 'city': 'Chennai', 'total_seats': 150, 'amenities': 'IMAX, 3D'},
            {'name': 'Escape Cinemas', 'location': 'Express Avenue', 'city': 'Chennai', 'total_seats': 80, 'amenities': '4DX'},
        ]
        theaters = []
        for t in theaters_data:
            obj, _ = Theater.objects.get_or_create(name=t['name'], defaults=t)
            theaters.append(obj)
        self.stdout.write('  ✓ Theaters created')

        # Movies
        movies_data = [
            {
                'title': 'Kalki 2898 AD',
                'description': 'A mythological sci-fi epic set in a dystopian future where an ancient prophecy collides with futuristic technology. The story follows the avatar of Vishnu in a post-apocalyptic world.',
                'duration': 181,
                'release_date': timezone.now().date() - timedelta(days=10),
                'rating': 'UA',
                'imdb_score': 7.2,
                'trailer_youtube_id': 'D3Hw9sIV3V8',
                'song_teaser_youtube_id': 'D3Hw9sIV3V8',
                'is_now_showing': True,
                'genre_names': ['Action', 'Sci-Fi', 'Drama'],
                'lang_names': ['Hindi', 'Telugu', 'Tamil'],
            },
            {
                'title': 'Pushpa 2: The Rule',
                'description': 'Puspha Raj expands his red sandalwood smuggling empire while facing new threats and enemies who challenge his iron rule.',
                'duration': 175,
                'release_date': timezone.now().date() - timedelta(days=5),
                'rating': 'A',
                'imdb_score': 7.8,
                'trailer_youtube_id': 'mq_HJXsGl_A',
                'song_teaser_youtube_id': 'mq_HJXsGl_A',
                'is_now_showing': True,
                'genre_names': ['Action', 'Drama', 'Thriller'],
                'lang_names': ['Hindi', 'Telugu', 'Tamil'],
            },
            {
                'title': 'Mufasa: The Lion King',
                'description': 'The origin story of Mufasa, exploring his journey from orphaned cub to one of the most beloved kings in the Pride Lands.',
                'duration': 118,
                'release_date': timezone.now().date() - timedelta(days=3),
                'rating': 'U',
                'imdb_score': 7.1,
                'trailer_youtube_id': 'O5GpGTLLl38',
                'song_teaser_youtube_id': 'O5GpGTLLl38',
                'is_now_showing': True,
                'genre_names': ['Animation', 'Drama'],
                'lang_names': ['Hindi', 'English', 'Tamil'],
            },
            {
                'title': 'Devara Part 1',
                'description': 'A fearless man builds a legacy of respect in coastal Andhra, but his son must face a new era of challenges and danger.',
                'duration': 166,
                'release_date': timezone.now().date() - timedelta(days=15),
                'rating': 'UA',
                'imdb_score': 6.8,
                'trailer_youtube_id': 'R8yGwCnf_ZA',
                'song_teaser_youtube_id': 'R8yGwCnf_ZA',
                'is_now_showing': True,
                'genre_names': ['Action', 'Drama'],
                'lang_names': ['Telugu', 'Hindi', 'Tamil'],
            },
            {
                'title': 'Oppenheimer',
                'description': 'The story of J. Robert Oppenheimer, the theoretical physicist who helped develop the first nuclear weapons during World War II.',
                'duration': 180,
                'release_date': timezone.now().date() - timedelta(days=30),
                'rating': 'UA',
                'imdb_score': 8.3,
                'trailer_youtube_id': 'uYPbbksJxIg',
                'song_teaser_youtube_id': 'uYPbbksJxIg',
                'is_now_showing': True,
                'genre_names': ['Drama', 'Thriller'],
                'lang_names': ['English', 'Hindi'],
            },
            {
                'title': 'KGF Chapter 3',
                'description': 'The saga continues as Rocky faces new threats to his empire, with enemies rising from every corner of the globe.',
                'duration': 0,
                'release_date': timezone.now().date() + timedelta(days=90),
                'rating': 'UA',
                'imdb_score': None,
                'trailer_youtube_id': 'WcTCPiXBiME',
                'song_teaser_youtube_id': 'WcTCPiXBiME',
                'is_now_showing': False,
                'is_coming_soon': True,
                'genre_names': ['Action', 'Drama'],
                'lang_names': ['Kannada', 'Hindi', 'Tamil'],
            },
            {
                'title': 'Animal Park',
                'description': 'The sequel to the blockbuster Animal continues the violent saga of Ranvijay Singh as he faces new enemies.',
                'duration': 0,
                'release_date': timezone.now().date() + timedelta(days=120),
                'rating': 'A',
                'imdb_score': None,
                'trailer_youtube_id': 'V7KCbSujFm0',
                'song_teaser_youtube_id': 'V7KCbSujFm0',
                'is_now_showing': False,
                'is_coming_soon': True,
                'genre_names': ['Action', 'Thriller'],
                'lang_names': ['Hindi'],
            },
            {
                'title': 'Stree 3',
                'description': 'The beloved horror-comedy franchise returns with more supernatural chaos in Chanderi.',
                'duration': 0,
                'release_date': timezone.now().date() + timedelta(days=60),
                'rating': 'UA',
                'imdb_score': None,
                'trailer_youtube_id': 'Ys1c0qgfSy8',
                'song_teaser_youtube_id': 'Ys1c0qgfSy8',
                'is_now_showing': False,
                'is_coming_soon': True,
                'genre_names': ['Comedy', 'Horror'],
                'lang_names': ['Hindi'],
            },
        ]

        now_showing_movies = []
        for m in movies_data:
            genre_names = m.pop('genre_names', [])
            lang_names = m.pop('lang_names', [])
            m.setdefault('is_coming_soon', False)

            movie, created = Movie.objects.get_or_create(
                title=m['title'],
                defaults=m
            )
            if not created:
                for field, value in m.items():
                    setattr(movie, field, value)
                movie.save()
            for gn in genre_names:
                if gn in genres:
                    movie.genres.add(genres[gn])
            for ln in lang_names:
                if ln in languages:
                    movie.languages.add(languages[ln])
            if movie.is_now_showing:
                now_showing_movies.append(movie)

        self.stdout.write('  ✓ Movies created')

        # Shows - create for next 7 days
        show_times = ['10:00', '13:30', '17:00', '20:30', '23:00']
        today = timezone.now().date()

        for movie in now_showing_movies:
            movie_langs = list(movie.languages.all())
            for day_offset in range(7):
                show_date = today + timedelta(days=day_offset)
                for theater in random.sample(theaters, min(3, len(theaters))):
                    for time_str in random.sample(show_times, 3):
                        h, m = map(int, time_str.split(':'))
                        show_dt = timezone.make_aware(
                            timezone.datetime(show_date.year, show_date.month, show_date.day, h, m)
                        )
                        lang = random.choice(movie_langs) if movie_langs else None
                        Show.objects.get_or_create(
                            movie=movie,
                            theater=theater,
                            show_time=show_dt,
                            defaults={
                                'language': lang,
                                'price_regular': random.choice([150, 180, 200]),
                                'price_premium': random.choice([280, 320, 350]),
                                'is_active': True
                            }
                        )

        self.stdout.write('  ✓ Shows created')

        # Create superuser if not exists
        if not CustomUser.objects.filter(email='admin@bookmyseat.com').exists():
            CustomUser.objects.create_superuser(
                username='admin',
                email='admin@bookmyseat.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write('  ✓ Superuser created: admin@bookmyseat.com / admin123')

        # Create demo user for testing
        if not CustomUser.objects.filter(email='demo@bms.com').exists():
            CustomUser.objects.create_user(
                username='demo',
                email='demo@bms.com',
                password='demo123',
                first_name='Demo',
                last_name='User'
            )
            self.stdout.write('  ✓ Demo user created: demo@bms.com / demo123')

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
        self.stdout.write('  Movies: ' + str(Movie.objects.count()))
        self.stdout.write('  Theaters: ' + str(Theater.objects.count()))
        self.stdout.write('  Shows: ' + str(Show.objects.count()))
