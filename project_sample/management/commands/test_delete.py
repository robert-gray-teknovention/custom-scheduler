try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from organizations.models import Organization
from custom_scheduler.models import Calendar, Staff, StaffTime, EventType
from custom_scheduler.models import CustomEvent as Event
from schedule.models import Occurrence


class Command(BaseCommand):
    help = "Delete the custom data except for super user"

    def handle(self, **options):
        users = User.objects.all().exclude(username='rgray')
        for u in users:
            print("Deleting User ", u.username)
            u.delete()
        print("Deleting all occurrences")
        Occurrence.objects.all().delete()
        for c in Calendar.objects.all():
            print("Deleting Cal ", c.name)
            c.delete()
        for o in Organization.objects.all():
            print("Deleting Org ", o.name)
            o.delete()
        print("Deleting Staff")
        Staff.objects.all().delete()
        print("Deleting Staff Time")
        StaffTime.objects.all().delete()
        print("Deleting Event Types")
        EventType.objects.all().delete()
        print("Deleting Events")
        Event.objects.all().delete()
