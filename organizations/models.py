from django.db import models
import pytz
# Create your models here.


class Organization(models.Model):
    def get_tuple_timezones(tzs):
        timezones = []
        for tz in tzs:
            timezones.append([tz, tz])
        return tuple(timezones)
    name = models.CharField(max_length=255)
    street1 = models.CharField(max_length=255, null=True)
    street2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, null=True)
    zip = models.CharField(max_length=10, null=True)
    state = models.CharField(max_length=2, null=True)
    phone = models.CharField(max_length=20, null=True)
    mailer_email = models.EmailField(max_length=255, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True, default='America/Los_Angeles',
                                choices=get_tuple_timezones(pytz.common_timezones)
                                )

    def __str__(self):
        return self.name
