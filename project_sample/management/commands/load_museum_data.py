try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load some sample data into the db"

    def handle(self, **options):
        import datetime
        from custom_scheduler.models import Calendar, Staff, StaffTime, EventType
        from custom_scheduler.models import CustomEvent as Event
        from schedule.models import Rule
        from schedule.models import Event as BaseEvent
        from organizations.models import Organization
        from django.contrib.auth.models import User
        from employee.models import TimesheetUser

        print("checking for existing data ...")
        try:
            cal = Calendar.objects.get(name="Custom Calendar")
            print("It looks like you already have loaded this custom data, quitting.")
            import sys
            sys.exit(1)
        except Calendar.DoesNotExist:
            print("Sample data not found in db.")
            print("Install it...")

        print("Create Custom Calendar ...")
        print("First create an organization user and TimesheetUser")
        org = Organization()
        org.name = 'Neighborhood North'
        org.save()

        user = User()
        user.username = "ccuser1"
        user.first_name = "CCUser"
        user.last_name = "TimesheetUser"
        user.email = "ccuser1@teknovention.com"
        user.password = "password1"
        user.save()

        user = User()
        user.username = "ccuser2"
        user.first_name = "CCUser2"
        user.last_name = "TimesheetUser2"
        user.email = "ccuser2@teknovention.com"
        user.password = "password2"
        user.save()

        tsuser = TimesheetUser()
        tsuser.user = user
        tsuser.save()
        cal = Calendar(name="Custom Calendar", slug="custom")
        cal.organization = org
        cal.save()
        print("The Custom Calendar is created.")
        print("Do we need to install the most common rules?")
        try:
            rule = Rule.objects.get(name="Daily")
        except Rule.DoesNotExist:
            print("Need to install the basic rules")
            rule = Rule(frequency="YEARLY", name="Yearly", description="will recur once every Year")
            rule.save()
            print("YEARLY recurrence created")
            rule = Rule(frequency="MONTHLY", name="Monthly", description="will recur once every Month")
            rule.save()
            print("Monthly recurrence created")
            rule = Rule(frequency="WEEKLY", name="Weekly", description="will recur once every Week")
            rule.save()
            print("Weekly recurrence created")
            rule = Rule(frequency="DAILY", name="Daily", description="will recur once every Day")
            rule.save()
            print("Daily recurrence created")
        print("Rules installed.")
        print("Install some Staff")
        try:
            staff = Staff.objects.get(user=User.objects.get(username='ccuser1'))
        except Staff.DoesNotExist:
            print("\tAdding Staff ccuser1")
            staff = Staff()
            staff.name = 'Custom Calendar User 1'
            staff.email = 'ccuser1@gmail.com'
            staff.phone = '555-448-5555'
            staff.staff_type = Staff.StaffType.HRL
            staff.user = User.objects.get(username='ccuser1')
            staff.organization = org
            staff.save()

            print("\tAdding Staff ccuser2")
            staff = Staff()
            staff.name = 'Custom Calendar User 2'
            staff.email = 'ccuser2@gmail.com'
            staff.phone = '555-448-6666'
            staff.staff_type = Staff.StaffType.BRD
            staff.user = User.objects.get(username='ccuser2')
            staff.organization = org
            staff.save()

        print("Install some event types")
        try:
            event_type = EventType.objects.get(name='Birthday Party')
            print("\tEventy Type is here")
        except EventType.DoesNotExist:
            print("We are adding event type Birthday Party")
            event_type = EventType()
            event_type.name = 'Birthday Party'
            event_type.organization = org
            event_type.save()
        try:
            event_type = EventType.objects.get(name='Staff Party')
            print("\tEvent Type is here")
        except EventType.DoesNotExist:
            print("We are adding event type Staff Party")
            event_type = EventType()
            event_type.name = 'Staff Party'
            event_type.organization = org
            event_type.save()

        today = datetime.date.today()

        print("Create some events")
        rule = Rule.objects.get(frequency="WEEKLY")
        data = {
            'title': 'Adam Birthday Party',
            'start': datetime.datetime(today.year, 11, 3, 8, 0),
            'end': datetime.datetime(today.year, 11, 3, 9, 0),
            'end_recurring_period': datetime.datetime(today.year + 30, 6, 1, 0, 0),
            'rule': rule,
            'calendar': cal
        }
        event = Event(**data)
        event.event_type = EventType.objects.get(name='Birthday Party')
        event.duration = 120
        event.save()

        ''' data = {
            'title': 'Exercise',
            'start': datetime.datetime(today.year, 11, 5, 15, 0),
            'end': datetime.datetime(today.year, 11, 5, 16, 30),
            'end_recurring_period': datetime.datetime(today.year + 20, 6, 1, 0, 0),
            'rule': rule,
            'calendar': cal
        }
        event = Event(**data)
        event.save()

        data = {
            'title': 'Exercise',
            'start': datetime.datetime(today.year, 11, 7, 8, 0),
            'end': datetime.datetime(today.year, 11, 7, 9, 30),
            'end_recurring_period': datetime.datetime(today.year + 20, 6, 1, 0, 0),
            'rule': rule,
            'calendar': cal
        }
        event = Event(**data)
        event.save()

        rule = Rule.objects.get(frequency="MONTHLY")
        data = {
            'title': 'Pay Mortgage',
            'start': datetime.datetime(today.year, today.month, today.day, 14, 0),
            'end': datetime.datetime(today.year, today.month, today.day, 14, 30),
            'end_recurring_period': datetime.datetime(today.year, today.month, today.day, 0, 0) + datetime.timedelta(days=1),
            'rule': rule,
            'calendar': cal
        }
        event = Event(**data)
        event.save()

        rule = Rule.objects.get(frequency="YEARLY")
        data = {
            'title': "Rock's Birthday Party",
            'start': datetime.datetime(today.year, today.month, today.day, 19, 0),
            'end': datetime.datetime(today.year, today.month, today.day, 23, 59),
            'end_recurring_period': datetime.datetime(today.year, today.month, today.day, 0, 0) + datetime.timedelta(days=1),
            'rule': rule,
            'calendar': cal
        }
        event = Event(**data)
        event.save()
        '''
        data = {
            'title': 'Christmas Party',
            'start': datetime.datetime(today.year, 12, 25, 19, 30),
            'end': datetime.datetime(today.year, 12, 25, 23, 59),
            'end_recurring_period': datetime.datetime(today.year + 2, 12, 31, 0, 0),
            'rule': rule,
            'calendar': cal
        }
        event = Event(**data)
        event.event_type = EventType.objects.get(name='Birthday Party')
        event.duration = 240
        event.save()

        '''data = {
            'title': 'New Pinax site goes live',
            'start': datetime.datetime(today.year + 1, 1, 6, 11, 0),
            'end': datetime.datetime(today.year + 1, 1, 6, 12, 00),
            'end_recurring_period': datetime.datetime(today.year + 2, 1, 7, 0, 0),
            'calendar': cal
        }
        event = Event(**data)
        event.save() '''

        print('Now add staffing to Occurrence')
        staff_time = StaffTime()
        staff_time.staff_member = Staff.objects.get(name='Custom Calendar User 1')
        # staff_time.start = datetime.datetime(today.year + 1, 1, 6, 11, 0),
        staff_time.start = datetime.datetime.now()
        # staff_time.end = datetime.datetime(today.year + 1, 1, 6, 13, 0),
        staff_time.end = datetime.datetime.now()
        event = BaseEvent.objects.get(title='Adam Birthday Party')
        staff_time.add(event)
        staff_time.save()

        print("Adding another staff time")
        staff_time = StaffTime()
        staff_time.staff_member = Staff.objects.get(name='Custom Calendar User 2')
        # staff_time.start = datetime.datetime(today.year + 1, 1, 6, 11, 0),
        staff_time.start = datetime.datetime.now()
        # staff_time.end = datetime.datetime(today.year + 1, 1, 6, 13, 0),
        staff_time.end = datetime.datetime.now()
        staff_time.add(event)
        staff_time.save()
