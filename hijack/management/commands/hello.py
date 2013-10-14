from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = '<name name ..>'
    help = 'Say hello to <name(s)>'

    def handle(self, *args, **options):
        for name in args:
            self.stdout.write('Hello %s.' % name)