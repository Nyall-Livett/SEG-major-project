from django.views.generic.list import ListView
from clubs.models import Notification

class NotificationListView(ListView):
    """View for all users notifications"""

    http_method_names = ['get']
    model = Notification
    template_name = 'notifications.html'

    def get_query_set(self, *args, **kwargs):
        notifications = Notification.objects.filter(receiver = self.request.user)
        return notifications
