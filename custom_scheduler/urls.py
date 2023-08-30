from django.views.generic import TemplateView
from custom_scheduler.views import EventViewAddChangeDelete
from django.conf.urls import include, url

urlpatterns = [
    url(r'^event/api/', EventViewAddChangeDelete.as_view(), name='event_api'),
]
