from django.shortcuts import render
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from .serializers import (
    UserSerializer,
    RuleSerializer,
    CustomEventSerializer,
    GetCustomEventSerializer,
    CalendarSerializer,
    OrganizationSerializer,
    EventTypeSerializer,
    StaffSerializer,
    StaffTimeSerializer,
    GetStaffTimeSerializer,
    OccurrenceSerializer,
    BaseEventSerializer,
    )
from custom_scheduler.models import CustomEvent, EventType, Calendar, Staff, StaffTime
from schedule.models.events import Occurrence, Event as BaseEvent
from schedule.models.rules import Rule
from organizations.models import Organization
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.http import require_POST
from django.db.models import F
from schedule.settings import (
    CHECK_EVENT_PERM_FUNC,
    CHECK_OCCURRENCE_PERM_FUNC,
)
from django.http import (
    JsonResponse,
)
import datetime
from schedule.utils import (
    check_calendar_permissions,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer


class CustomEventViewSet(viewsets.ModelViewSet):
    queryset = CustomEvent.objects.all()
    serializer_class = GetCustomEventSerializer

    def get_serializer_class(self):
        # Use SerializerForGET for GET requests
        if self.request.method == 'GET':
            print("We are getting a serializer class")
            return GetCustomEventSerializer
        # Use SerializerForPOST for POST requests
        elif self.request.method == 'POST' or self.request.method == 'PUT':
            return CustomEventSerializer
        # Use the default serializer for other HTTP methods
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        # Override get_serializer to pass the request context to the serializer
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
    # serializer_class = CustomEventSerializer


class BaseEventViewSet(viewsets.ModelViewSet):
    queryset = BaseEvent.objects.all()
    serializer_class = BaseEventSerializer

    '''@action(detail=False, methods=['GET'], url_path='occurrence')
    def occurrence_detail(self, request, pk=None):
        event = self.get_object()
        serializer = BaseEventSerializer(, many=False, context={'request': request})
        return Response(serializer.data)'''


class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    @action(detail=True, methods=['GET'], url_path='events_list')
    def events_list(self, request, pk=None):
        calendar = self.get_object()
        events = calendar.event_set.all()
        serializer = BaseEventSerializer(events, many=True, context={'request': request})
        return Response(serializer.data)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StaffTimeViewSet(viewsets.ModelViewSet):
    queryset = StaffTime.objects.all()

    def get_serializer_class(self):
        # Use SerializerForGET for GET requests
        if self.request.method == 'GET':
            return GetStaffTimeSerializer
        # Use SerializerForPOST for POST requests
        elif self.request.method == 'POST':
            return StaffTimeSerializer
        # Use the default serializer for other HTTP methods
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        # Override get_serializer to pass the request context to the serializer
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = StaffTimeSerializer(context={'request': request}, data=request.data)
        # print(str(serializer.initial_data))

        if serializer.is_valid():
            st = serializer.save()
            st.add_occurrence()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OccurrenceViewSet(viewsets.ModelViewSet):
    queryset = Occurrence.objects.all()
    serializer_class = OccurrenceSerializer


@require_POST
@check_calendar_permissions
def api_move_or_resize_by_code(request):
    response_data = {}
    user = request.user
    id = request.POST.get("id")
    existed = bool(request.POST.get("existed") == "true")
    delta = datetime.timedelta(minutes=int(request.POST.get("delta")))
    resize = bool(request.POST.get("resize", False))
    event_id = request.POST.get("event_id")

    response_data = _api_move_or_resize_by_code(
        user, id, existed, delta, resize, event_id
    )

    return JsonResponse(response_data)


def _api_move_or_resize_by_code(user, id, existed, delta, resize, event_id):
    print("hello we switched!!!")
    response_data = {}
    response_data["status"] = "PERMISSION DENIED"

    if existed:
        occurrence = Occurrence.objects.get(id=id)
        occurrence.end += delta
        if not resize:
            occurrence.start += delta
        if CHECK_OCCURRENCE_PERM_FUNC(occurrence, user):
            occurrence.save()
            response_data["status"] = "OK"
    else:
        event = CustomEvent.objects.get(id=event_id)
        dts = 0
        dte = delta
        if not resize:
            event.start += delta
            dts = delta
        event.end = event.end + delta
        print("Start ", event.start)
        print("End ", event.end)
        if CHECK_EVENT_PERM_FUNC(event, user):
            event.save()
            print("num of occurrences ", event.occurrence_set.all().count())
            '''event.occurrence_set.all().update(
                original_start=F("original_start") + dts,
                original_end=F("original_end") + dte,
            )'''
            response_data["status"] = "OK"
    return response_data
