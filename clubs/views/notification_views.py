from django.views.generic.list import ListView


class NotificationListView(ListView):
    """View for all users notifications"""

    http_method_names = ['get']
    model = Notification
    template_name = 'notifications.html'

    def setup(self, request, *args, **kwargs):
        print("hello")
