"""
Django management command to seed the database with sample events.

Usage:
    python manage.py seed_events
    python manage.py seed_events --clear  # Clear existing events first
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta, time
from barlery.models import Event


class Command(BaseCommand):
    help = 'Seeds the database with sample events for development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing events before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing events...')
            Event.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ All events cleared'))

        self.stdout.write('Seeding events...')

        # Get today's date
        today = timezone.now().date()

        # Sample events data
        events_data = [
            {
                'title': 'Live Jazz Night with The Riverside Trio',
                'date': today + timedelta(days=3),
                'start_time': time(20, 0),  # 8:00 PM
                'end_time': time(23, 0),    # 11:00 PM
                'description': 'Join us for an intimate evening of smooth jazz with The Riverside Trio. Experience classic standards and modern interpretations in our cozy venue. Cover charge: $10 at the door.',
            },
            {
                'title': 'Open Mic Night',
                'date': today + timedelta(days=7),
                'start_time': time(19, 0),  # 7:00 PM
                'end_time': time(22, 0),    # 10:00 PM
                'description': 'Showcase your talent! Sign-ups start at 6:30 PM. Musicians, poets, comedians - all are welcome. Free entry for performers and audience.',
            },
            {
                'title': 'Trivia Tuesday: 90s Pop Culture Edition',
                'date': today + timedelta(days=10),
                'start_time': time(19, 30),  # 7:30 PM
                'end_time': time(21, 30),    # 9:30 PM
                'description': 'Test your knowledge of 90s movies, music, TV shows, and more! Teams of up to 6 people. Prizes for top 3 teams. No cover charge.',
            },
            {
                'title': 'The Electric Strings - Rock Cover Band',
                'date': today + timedelta(days=14),
                'start_time': time(21, 0),  # 9:00 PM
                'end_time': time(1, 0),     # 1:00 AM (next day)
                'description': 'High-energy rock covers from the 70s to today! The Electric Strings bring down the house with classic hits and modern favorites. $15 cover.',
            },
            {
                'title': 'Craft Beer Tasting Event',
                'date': today + timedelta(days=17),
                'start_time': time(18, 0),  # 6:00 PM
                'end_time': time(20, 0),    # 8:00 PM
                'description': 'Sample 8 local craft beers from Tennessee breweries. Learn about brewing processes and flavor profiles. Limited to 30 participants. $25 includes all tastings and light appetizers.',
            },
            {
                'title': 'Acoustic Sunday with Sarah Mitchell',
                'date': today + timedelta(days=21),
                'start_time': time(18, 0),  # 6:00 PM
                'end_time': time(20, 0),    # 8:00 PM
                'description': 'Singer-songwriter Sarah Mitchell performs original folk songs and acoustic covers. Perfect Sunday evening vibes. No cover, tips appreciated.',
            },
            {
                'title': 'Karaoke Night',
                'date': today + timedelta(days=24),
                'start_time': time(20, 0),  # 8:00 PM
                'end_time': time(23, 30),   # 11:30 PM
                'description': 'Sing your heart out! Full karaoke system with thousands of songs. Private rooms available for groups. No cover charge.',
            },
            {
                'title': 'The Blues Brothers Tribute Band',
                'date': today + timedelta(days=28),
                'start_time': time(21, 0),  # 9:00 PM
                'end_time': time(23, 30),   # 11:30 PM
                'description': 'A high-energy tribute to Jake and Elwood! Full costumes, choreography, and all your favorite hits from the classic film. $12 cover.',
            },
            {
                'title': 'Local Artist Showcase',
                'date': today + timedelta(days=31),
                'start_time': time(19, 0),  # 7:00 PM
                'end_time': time(22, 0),    # 10:00 PM
                'description': 'Featuring 5 up-and-coming local artists across genres from indie rock to R&B. Support your local music scene! $8 cover, all proceeds go to performers.',
            },
            {
                'title': 'Comedy Night with Mike Henderson',
                'date': today + timedelta(days=35),
                'start_time': time(20, 30),  # 8:30 PM
                'end_time': time(22, 30),    # 10:30 PM
                'description': 'Stand-up comedy featuring headliner Mike Henderson and special guests. 21+ only. $15 cover includes one drink ticket.',
            },
            {
                'title': 'New Years Eve Celebration',
                'date': today + timedelta(days=40),
                'start_time': time(21, 0),  # 9:00 PM
                'end_time': time(2, 0),     # 2:00 AM (next day)
                'description': 'Ring in the new year at Barlery! Live DJ, champagne toast at midnight, party favors, and dancing all night. Advanced tickets recommended. $30 cover.',
            },
            {
                'title': 'Vinyl Night: Classic Rock Edition',
                'date': today + timedelta(days=45),
                'start_time': time(18, 30),  # 6:30 PM
                'end_time': time(21, 0),     # 9:00 PM
                'description': 'Bring your favorite vinyl records or enjoy selections from our collection. We spin classic rock albums on our vintage turntable. Free event.',
            },
        ]

        # Create events
        created_count = 0
        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                date=event_data['date'],
                defaults=event_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'  ✓ Created: {event.title} on {event.date}')
            else:
                self.stdout.write(f'  - Skipped (already exists): {event.title}')

        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully seeded {created_count} events!'))
        self.stdout.write(f'Total events in database: {Event.objects.count()}')