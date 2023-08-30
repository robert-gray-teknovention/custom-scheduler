from django.views.generic import TemplateView
from custom_scheduler.views import CalendarView
from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
from django.conf import settings


admin.autodiscover()

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="homepage.html"),),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^fullcalendar/', CalendarView.as_view(template_name="fullcalendar.html"), name='fullcalendar'),
    url(r'^admin/', admin.site.urls),
    url(r'^customschedule/', include('custom_scheduler.urls')),
    path('apis/', include('apis.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
