# import serializer from rest_framework
from rest_framework import serializers
from custom_scheduler.models import CustomEvent as Event, Calendar, EventType, Staff, StaffTime
from organizations.models import Organization
from schedule.models.events import Occurrence, Event as BaseEvent


class BaseEventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BaseEvent
        fields = ('url', 'id', 'title', 'description', 'start', 'end', 'calendar')


class EventSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Event
        fields = ('url', 'id', 'title', 'description', 'start', 'end', 'duration', 'calendar', 'event_type')


class CalendarSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Calendar
        fields = ('url', 'id', 'name', 'slug', 'organization')


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Organization
        fields = ('__all__')


class EventTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventType
        fields = ('__all__')


class StaffSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Staff
        fields = ('url', 'id', 'name', 'email', 'phone', 'staff_type', 'organization')


class StaffTimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StaffTime
        fields = ('__all__')


class OccurrenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Occurrence
        fields = ('url', 'event', 'title', 'description', 'start', 'end', 'original_start', 'original_end',
                  'created_on',
                  'updated_on',
                  'staffing')
