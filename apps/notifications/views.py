from rest_framework.response import Response
from rest_framework.views import APIView
from apps.notifications.events.notification_created import NotificationCreatedEvent
from core.events.dispatcher import EventDispatcher



class DevelopmentView(APIView):
    def get(self, request):
        event = NotificationCreatedEvent(
            event_id='dfd',
            notification_id="dfsdlfj",
            recipient_id="dsfsd",
            title="title",
            body="body"
        )

        print('Event Created')

        EventDispatcher.dispatch(event=event)

        print('Event Dispatched')

        return Response(data={'data': "Running"})