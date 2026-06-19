from django.core.management.base import BaseCommand
from django.utils import timezone
from movies.models import Show
import datetime


class Command(BaseCommand):
    help = (
        "Shift all Show.show_time datetimes forward so shows become future events.\n"
        "By default the command computes the minimal days to add so that the earliest show is tomorrow."
    )

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, help='Number of days to add to each show_time')
        parser.add_argument('--dry-run', action='store_true', help='Do not save changes; only print what would change')

    def handle(self, *args, **options):
        days = options.get('days')
        dry_run = options.get('dry_run', False)

        now = timezone.now()
        qs = Show.objects.all()
        if not qs.exists():
            self.stdout.write('No shows found in database.')
            return

        first = qs.order_by('show_time').first()
        min_dt = first.show_time

        if days is None:
            # Compute days to add so earliest show moves to tomorrow
            delta_days = (now.date() - min_dt.date()).days + 1
            days = max(delta_days, 0)

        if days <= 0:
            self.stdout.write('No shift needed (days <= 0).')
            return

        self.stdout.write(f'Applying shift of {days} day(s) to {qs.count()} shows (dry_run={dry_run})')

        changed = 0
        for show in qs:
            old = show.show_time
            new = old + datetime.timedelta(days=days)
            if dry_run:
                self.stdout.write(f'#{show.id} {show.movie.title}: {old.isoformat()} -> {new.isoformat()}')
            else:
                show.show_time = new
                show.save(update_fields=['show_time'])
                changed += 1

        if dry_run:
            self.stdout.write('Dry run complete; no changes saved.')
        else:
            self.stdout.write(f'Successfully updated {changed} shows.')
