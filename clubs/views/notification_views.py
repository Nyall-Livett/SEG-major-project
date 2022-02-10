from django.views.generic.list import ListView
from clubs.models import Notification
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


class NotificationListView(LoginRequiredMixin, ListView):
    """View for all users notifications"""

    http_method_names = ['get']
    template_name = 'notifications.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.request.user.notification_set.all().update(read=True)

    def get_queryset(self):
        query_set = self.request.user.notification_set.all()
        return query_set.order_by('-created_on')

class NotificationMarkAllActedUpon(LoginRequiredMixin, View):

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            notifications = request.POST.get('notifications')
            parsedIds = json.loads(notifications)
            notificationArray = []
            for notification_id in parsedIds:
                notification = Notification.objects.get(id=notification_id)
                if notification is not None:
                    notification.acted_upon = True
                    notificationArray.append(notification)
            Notification.objects.bulk_update(notificationArray, ['acted_upon'])
            return JsonResponse({}, status=200)

class NotificationMarkAllNotActedUpon(LoginRequiredMixin, View):

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            notifications = request.POST.get('notifications')
            parsedIds = json.loads(notifications)
            notificationArray = []
            for notification_id in parsedIds:
                notification = Notification.objects.get(id=notification_id)
                if notification is not None:
                    notification.acted_upon = False
                    notificationArray.append(notification)
            Notification.objects.bulk_update(notificationArray, ['acted_upon'])
            return JsonResponse({}, status=200)

class NotificationDelete(LoginRequiredMixin, View):

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            notifications = request.POST.get('notifications')
            parsedIds = json.loads(notifications)
            notificationArray = []
            for notification_id in parsedIds:
                notification = Notification.objects.get(id=notification_id)
                if notification is not None:
                    notification.delete()
            return JsonResponse({}, status=200)
