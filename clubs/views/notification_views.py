from django.views.generic.list import ListView
from clubs.models import Notification
class NotificationListView(ListView):
    """View for all users notifications"""

    http_method_names = ['get']
    model = Notification
    template_name = 'notifications.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.request.user.notification_set.all().update(read=True)

    def get_query_set(self, *args, **kwargs):
        notifications = Notification.objects.filter(receiver = self.request.user)
        return notifications
