import csv
from django.core.management.base import BaseCommand
from apps.eventManager.models import Stadium, Event
from django.utils.dateparse import parse_datetime


class Command(BaseCommand):
    help = "Import Stadium and Event data from Mockaroo CSV files."

    def add_arguments(self, parser):
        parser.add_argument(
            '--stadiums',
            type=str,
            help="home/shio/downloads/mock_stadiums.csv",
            required=True
        )
        parser.add_argument(
            '--events',
            type=str,
            help="home/shio/downloads/mock_events.csv",
            required=True
        )

    def handle(self, *args, **kwargs):
        stadiums_file = kwargs['stadiums']
        events_file = kwargs['events']

        # Import stadiums
        self.stdout.write("Importing stadiums...")
        with open(stadiums_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Stadium.objects.update_or_create(
                    id=row['id'],  # Assuming ID is included in the CSV
                    defaults={
                        'name': row['name'],
                        'address': row['address'],
                        'capacity': int(row['capacity']),
                    }
                )
        self.stdout.write("Stadiums imported successfully!")

        # Import events
        self.stdout.write("Importing events...")
        with open(events_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    stadium = Stadium.objects.get(id=row['stadium_id'])  # Foreign key
                except KeyError as e:
                    stadium = None
                Event.objects.update_or_create(
                    id=row['id'],  # Assuming ID is included in the CSV
                    defaults={
                        'name': row['name'],
                        'date': parse_datetime(row['date']),
                        'stadium': stadium,
                        'is_active': True,
                    }
                )
        self.stdout.write("Events imported successfully!")
