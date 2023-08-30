from django.contrib import admin
from .models import TimesheetUser


class ApproveesInLine(admin.TabularInline):
    model = TimesheetUser.approvees.through
    extra = 1
    fk_name = "from_timesheetuser"


class TimesheetUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'organization', 'hourly_rate')
    inlines = [
        ApproveesInLine,
    ]


admin.site.register(TimesheetUser, TimesheetUserAdmin)
