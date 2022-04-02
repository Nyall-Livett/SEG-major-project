"""User related views."""
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from clubs.factories.moment_factory import CreateMoment
from clubs.models import Moment, User, Club, BooksRead, Notification
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from clubs.factories.notification_factory import CreateNotification, NotificationType
from clubs.enums import MomentType
from django.contrib import messages


class UserListView(LoginRequiredMixin, ListView):
    """View that shows a list of all users."""

    model = User
    template_name = "user_list.html"
    context_object_name = "users"
    paginate_by = settings.USERS_PER_PAGE

class MemberListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "member_list.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        """Return context data, including new post form."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['club'] = Club.objects.get(id=self.kwargs.get('club_id'))

        return context

class FollowRequestsListView(LoginRequiredMixin, ListView):
    """View that show a list of all follow requests."""

    model = User
    template_name = "follow_requests.html"
    context_object_name = "follow_requests"
    paginate_by = settings.USERS_PER_PAGE

    def get(self,request, optional_notification="", *args, **kwargs):
        if optional_notification:
            notification = Notification.objects.get(id=optional_notification)
            if notification.receiver == request.user and notification.acted_upon == False:
                notification.acted_upon = True
                notification.save()
        return super().get(self,request, optional_notification, *args, **kwargs)

    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)
        context['follow_requests'] = self.request.user.follow_requests.all()
        return context

class FollowersListView(LoginRequiredMixin, ListView):
    """View that show a list of all followers."""

    model = User
    template_name = "followers.html"
    context_object_name = "followers"
    paginate_by = settings.USERS_PER_PAGE

    def dispatch(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=self.kwargs['user_id'])
        except ObjectDoesNotExist:
            return redirect('user_list')
        else:
            return super(FollowersListView, self).get(request, *args, **kwargs)

    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)
        user_id = self.kwargs['user_id']
        user = User.objects.get(pk=user_id)
        followers = user.followers.all()
        context['followers'] = followers
        return context

class FollowingListView(LoginRequiredMixin, ListView):
    """View that show a list of all followers."""

    model = User
    template_name = "followee.html"
    context_object_name = "followees"
    paginate_by = settings.USERS_PER_PAGE

    def dispatch(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=self.kwargs['user_id'])
        except ObjectDoesNotExist:
            return redirect('user_list')
        else:
            return super(FollowingListView, self).get(request, *args, **kwargs)

    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)
        user_id = self.kwargs['user_id']
        user = User.objects.get(pk=user_id)
        followees = user.followees.all()
        context['followees'] = followees
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
        context['reviews'] = BooksRead.objects.all()
        context['moments'] = Moment.objects.all().order_by('-created_on')[:5]
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
        notifier = CreateNotification()
        notifier.notify(NotificationType.FOLLOW_REQUEST, followee_request, {'user': request.user})
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
        moment_notifier = CreateMoment()
        moment_notifier.notify(MomentType.BECAME_FRIENDS, logged_in_user, {'other_user': followee_request, 'body':''})
        moment_notifier.notify(MomentType.BECAME_FRIENDS, followee_request, {'other_user': logged_in_user, 'body': '{user} has accepted your follow request'.format(user=logged_in_user)})
        messages.add_message(request, messages.SUCCESS, "You have successfully accepted follow request from {user}".format(user=followee_request.username))
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
        messages.add_message(request, messages.SUCCESS, "You have successfully rejected follow request from {user}".format(user=followee_request.username))
    except ObjectDoesNotExist:
        return redirect('follow_requests_page')
    else:
        return redirect('follow_requests_page')
