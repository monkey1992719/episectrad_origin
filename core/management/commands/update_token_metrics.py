from django.core.management.base import BaseCommand

from ... import tasks


class Command(BaseCommand):
    help = "Update token metrics"  # noqa: A003,B003

    def handle(self, *args, **options):
        tasks.update_token_metrics()
        self.stdout.write("Done\n")
