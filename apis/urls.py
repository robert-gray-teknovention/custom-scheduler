from django.urls import include, path
# import routers
from rest_framework import routers

# import everything from views
from .views import EventViewSet, CalendarViewSet, OrganizationViewSet, EventTypeViewSet, StaffViewSet, StaffTimeViewSet
from .views import OccurrenceViewSet, BaseEventViewSet, api_move_or_resize_by_code
router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'event_bases', BaseEventViewSet)
router.register(r'calendars', CalendarViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'event_types', EventTypeViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'staff_times', StaffTimeViewSet)
router.register(r'occurrences', OccurrenceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('move_or_resize/?', api_move_or_resize_by_code, name='api_move_or_resize_custom')
]
