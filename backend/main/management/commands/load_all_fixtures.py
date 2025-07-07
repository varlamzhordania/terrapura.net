from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Load all fixtures from a directory (default: BASE_DIR/fixtures)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='Optional path to the directory containing fixture files',
        )

    def handle(self, *args, **options):
        path = options['path']
        fixtures_dir = Path(path) if path else Path(settings.BASE_DIR) / "fixtures"

        if not fixtures_dir.exists() or not fixtures_dir.is_dir():
            raise CommandError(f"Fixtures directory not found: {fixtures_dir}")

        fixture_files = sorted(fixtures_dir.glob("*.json"))

        if not fixture_files:
            self.stdout.write(self.style.WARNING("No .json fixture files found in the directory."))
            return

        self.stdout.write(self.style.SUCCESS(f"📦 Found {len(fixture_files)} fixture(s) in {fixtures_dir}"))

        for fixture_file in fixture_files:
            try:
                self.stdout.write(f"➡️  Loading {fixture_file.name}...")
                call_command('loaddata', str(fixture_file))
                self.stdout.write(self.style.SUCCESS(f"✅ Loaded {fixture_file.name}"))
            except Exception as e:
                raise CommandError(f"❌ Failed to load {fixture_file.name}: {e}")
