from django.db import models
from django.contrib.auth.models import User
from organizations.models import Organization


class TimesheetUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    approvers = models.ManyToManyField("self", blank=True, symmetrical=False, related_name='approvees')
    org_manager = models.ManyToManyField(Organization, blank=True, related_name='managers')

    def __str__(self):
        name = self.user.username
        return name
