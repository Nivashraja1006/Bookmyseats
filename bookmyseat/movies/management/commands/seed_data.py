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
                'title': 'Kara',
                'description': 'Set in early 1990s Tamil Nadu, a reformed thief named Kara is forced back into crime after his family\'s ancestral land is seized by a corrupt bank official. Starring Dhanush, Mamitha Baiju, Jayaram and Suraj Venjaramoodu in a gripping heist action thriller directed by Vignesh Raja with music by GV Prakash Kumar.',
                'duration': 161,
                'release_date': timezone.now().date() - timedelta(days=51),
                'rating': 'UA',
                'imdb_score': 7.5,
                'trailer_youtube_id': 'mEtGQOTrsU4',
                'song_teaser_youtube_id': 'mEtGQOTrsU4',
                'is_now_showing': True,
                'genre_names': ['Action', 'Thriller', 'Drama'],
                'lang_names': ['Tamil', 'Telugu', 'Hindi'],
            },
            {
                'title': 'Karuppu',
                'description': 'The guardian deity Vettai Karuppu disguises himself as a rural lawyer named Saravanan to battle injustice and corruption in a court system exploiting a young girl. Starring Suriya and Trisha Krishnan in a high-octane fantasy action film directed by RJ Balaji with music by Sai Abhyankkar.',
                'duration': 152,
                'release_date': timezone.now().date() - timedelta(days=36),
                'rating': 'UA',
                'imdb_score': 7.0,
                'trailer_youtube_id': 'JpVl_-1YgIo',
                'song_teaser_youtube_id': 'JpVl_-1YgIo',
                'is_now_showing': True,
                'genre_names': ['Action', 'Drama', 'Thriller'],
                'lang_names': ['Tamil', 'Telugu', 'Hindi'],
            },
            {
                'title': '29',
                'description': 'A coming-of-age romantic drama about a man lost in the search for his identity who spends his life chasing answers. Starring Vidhu and Preethi Asrani, directed by Rathna Kumar and produced by Karthik Subbaraj and Lokesh Kanagaraj.',
                'duration': 150,
                'release_date': timezone.now().date() - timedelta(days=43),
                'rating': 'UA',
                'imdb_score': 7.4,
                'trailer_youtube_id': 'qWSGdwHeKD4',
                'song_teaser_youtube_id': 'qWSGdwHeKD4',
                'is_now_showing': True,
                'genre_names': ['Drama', 'Romance'],
                'lang_names': ['Tamil', 'Telugu', 'Hindi'],
            },
            {
                'title': 'Youth',
                'description': 'A feel-good romantic comedy about Praveen, a carefree 16-year-old boy determined to find the love of his life before school ends. Written, directed and performed by Ken Karunas with music by GV Prakash Kumar.',
                'duration': 141,
                'release_date': timezone.now().date() - timedelta(days=93),
                'rating': 'U',
                'imdb_score': 8.1,
                'trailer_youtube_id': 'X83zWEDRbCU',
                'song_teaser_youtube_id': 'X83zWEDRbCU',
                'is_now_showing': True,
                'genre_names': ['Comedy', 'Romance', 'Drama'],
                'lang_names': ['Tamil', 'Telugu', 'Hindi'],
            },
            {
                'title': 'Double Occupancy',
                'description': 'Rajini, due to an anomaly during birth, lives as a female from 6am to 6pm and as a male from 6pm to 6am. This unique gender-swap fantasy romantic comedy explores the hilarious complications when Rajini tries to hide this condition from two different partners. Directed by Aswin Kandasamy with music by Sam C.S.',
                'duration': 130,
                'release_date': timezone.now().date() - timedelta(days=9),
                'rating': 'UA',
                'imdb_score': 7.2,
                'trailer_youtube_id': '6QNUFgR2HLk',
                'song_teaser_youtube_id': '6QNUFgR2HLk',
                'is_now_showing': True,
                'genre_names': ['Comedy', 'Romance'],
                'lang_names': ['Tamil'],
            },
            {
                'title': 'Nooru Saami',
                'description': 'A powerful Tamil drama about a woman fighting for her rights and dignity in a village dominated by caste and patriarchy. Starring Vijay Antony, Swasika, Ajay Dhishan and Lijomol Jose in pivotal roles. Directed by Sasi with music by Balaji Sriram.',
                'duration': 131,
                'release_date': timezone.now().date() - timedelta(days=2),
                'rating': 'UA',
                'imdb_score': 7.3,
                'trailer_youtube_id': '3EGuYn0_VXc',
                'song_teaser_youtube_id': '3EGuYn0_VXc',
                'is_now_showing': True,
                'genre_names': ['Drama'],
                'lang_names': ['Tamil'],
            },
            {
                'title': 'Parimala and Co',
                'description': 'A dysfunctional family becomes prime suspects in a murder connected to their household. Starring Jayaram, Urvashi, Mysskin, Yogi Babu and Sandy in this black comedy thriller directed by Pandiraaj. The family\'s peaceful life is disrupted when a local rowdy begins harassing their younger daughter.',
                'duration': 146,
                'release_date': timezone.now().date() - timedelta(days=16),
                'rating': 'UA',
                'imdb_score': 6.8,
                'trailer_youtube_id': 'KPliGJj6In4',
                'song_teaser_youtube_id': 'KPliGJj6In4',
                'is_now_showing': True,
                'genre_names': ['Comedy', 'Thriller'],
                'lang_names': ['Tamil'],
            },
            {
                'title': 'Engal Thangam',
                'description': 'In a deeply traditional household, a quiet woman struggles to find acceptance while harboring a dark hidden past. When unexpected danger from her former life threatens her new family, she must shed her docile exterior. Starring Samantha Ruth Prabhu and Gulshan Devaiah, directed by Nandini Reddy with music by Santhosh Narayanan.',
                'duration': 154,
                'release_date': timezone.now().date() - timedelta(days=2),
                'rating': 'UA',
                'imdb_score': 7.6,
                'trailer_youtube_id': 'smfHL8sgBEU',
                'song_teaser_youtube_id': 'smfHL8sgBEU',
                'is_now_showing': True,
                'genre_names': ['Action', 'Thriller', 'Drama'],
                'lang_names': ['Tamil', 'Telugu', 'Hindi'],
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
            {
                'title': 'Om Chapter 1',
                'description': 'A fearless guardian fights armed assailants in a rain-soaked forest to protect innocent villagers. Starring Dhanush, Mammootty, Sai Pallavi and Sreeleela, this high-octane action drama explores social unrest and revolution. Directed by Rajkumar Periasamy.',
                'duration': 0,
                'release_date': timezone.now().date() + timedelta(days=118),
                'rating': 'UA',
                'imdb_score': None,
                'trailer_youtube_id': 'D5ZJl7vaE4k',
                'song_teaser_youtube_id': 'D5ZJl7vaE4k',
                'is_now_showing': False,
                'is_coming_soon': True,
                'genre_names': ['Action', 'Thriller'],
                'lang_names': ['Tamil', 'Telugu', 'Hindi'],
            },
            {
                'title': 'Cars 4',
                'description': 'Lightning McQueen and his friends are back for an all-new adventure! Blindsided by a new generation of blazing-fast electric racers, the legendary Lightning McQueen must adapt or be left behind. A thrilling Disney Pixar sequel.',
                'duration': 0,
                'release_date': timezone.now().date() + timedelta(days=150),
                'rating': 'U',
                'imdb_score': None,
                'trailer_youtube_id': 'Q6wjTQLWDJQ',
                'song_teaser_youtube_id': 'Q6wjTQLWDJQ',
                'is_now_showing': False,
                'is_coming_soon': True,
                'genre_names': ['Animation', 'Comedy'],
                'lang_names': ['English', 'Hindi', 'Tamil'],
            },
            {
                'title': 'The Paradise',
                'description': 'In 1980s Secunderabad, a marginalized tribe battles discrimination and fights for citizenship under an unexpected leader\'s guidance. Starring Nani and Janhvi Kapoor, directed by Srikanth Odela with music by Anirudh Ravichander.',
                'duration': 0,
                'release_date': timezone.now().date() + timedelta(days=62),
                'rating': 'UA',
                'imdb_score': None,
                'trailer_youtube_id': 'NkZFnpDhdCk',
                'song_teaser_youtube_id': 'NkZFnpDhdCk',
                'is_now_showing': False,
                'is_coming_soon': True,
                'genre_names': ['Action', 'Drama', 'Thriller'],
                'lang_names': ['Telugu', 'Hindi', 'Tamil'],
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

        if not CustomUser.objects.filter(email='admin@bookmyseat.com').exists():
            CustomUser.objects.create_superuser(
                username='admin',
                email='admin@bookmyseat.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write('  ✓ Superuser created: admin@bookmyseat.com / admin123')

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