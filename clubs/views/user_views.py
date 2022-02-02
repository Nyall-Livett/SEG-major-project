"""User related views."""
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.list import MultipleObjectMixin
from clubs.models import User

class UserListView(LoginRequiredMixin, ListView):
    """View that shows a list of all users."""

    model = User
    template_name = "user_list.html"
    context_object_name = "users"
    paginate_by = settings.USERS_PER_PAGE

class ShowUserView(LoginRequiredMixin, DetailView):
    """View that shows individual user details."""

    model = User
    template_name = 'show_user.html'
    pk_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        """Handle get request, and redirect to user_list if user_id invalid."""

        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return redirect('user_list')

    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)
        user = self.get_object()
        context['following'] = self.request.user.is_following(user)
        return context


def follow_toggle(request):
    return redirect('home')