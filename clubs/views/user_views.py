"""User related views."""
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.list import MultipleObjectMixin
from clubs.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

class UserListView(LoginRequiredMixin, ListView):
    """View that shows a list of all users."""

    model = User
    template_name = "user_list.html"
    context_object_name = "users"
    paginate_by = settings.USERS_PER_PAGE

class FollowRequestsListView(LoginRequiredMixin, ListView):
    """View that show a list of all follow requests."""

    model = User
    template_name = "follow_requests.html"
    context_object_name = "follow_requests"
    paginate_by = settings.USERS_PER_PAGE

    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)
        context['follow_requests'] = self.request.user.follow_requests.all()
        return context

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
        context['request_sent'] = self.request.user.is_request_sent(user)
        return context

@login_required
def follow_toggle(request, user_id):
    logged_in_user = request.user
    try:
        followee = User.objects.get(id=user_id)
        logged_in_user.toggle_follow(followee)
    except ObjectDoesNotExist:
        return redirect('user_list')
    else:
        return redirect('show_user', user_id=user_id)

@login_required
def follow_request(request, user_id):
    logged_in_user = request.user
    try:
        followee_request = User.objects.get(id=user_id)
        logged_in_user.send_follow_request(followee_request)
    except ObjectDoesNotExist:
        return redirect('user_list')
    else:
        return redirect('show_user', user_id=user_id)

@login_required
def accept_request(request, user_id):
    logged_in_user = request.user
    try:
        followee_request = User.objects.get(id=user_id)
        logged_in_user.accept_request(followee_request)
    except ObjectDoesNotExist:
        return redirect('follow_requests_page')
    else:
        return redirect('show_user', user_id=user_id)

@login_required
def reject_request(request, user_id):
    logged_in_user = request.user
    try:
        followee_request = User.objects.get(id=user_id)
        logged_in_user.reject_request(followee_request)
    except ObjectDoesNotExist:
        return redirect('follow_requests_page')
    else:
        return redirect('follow_requests_page')